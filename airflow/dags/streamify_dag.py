import os
from datetime import datetime

from airflow.operators.bash import BashOperator
from schema import schema
from task_templates import (create_empty_table, create_external_table,
                            delete_external_table, insert_job)

from airflow import DAG

EVENT = 'spotify' 


GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'stg_dataset')
EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d%H") }}'
TABLE_MAP = {'SPOTIFY_TABLE': 'spotify'}
MACRO_VARS = {"GCP_PROJECT_ID":GCP_PROJECT_ID, 
              "BIGQUERY_DATASET": BIGQUERY_DATASET, 
              "EXECUTION_DATETIME_STR": EXECUTION_DATETIME_STR
              }
MACRO_VARS.update(TABLE_MAP)
default_args = {
    'owner' : 'airflow'
}
with DAG(
    dag_id = f'streamify_dag',
    default_args = default_args,
    description = f'Hourly data pipeline to generate dims and facts for streamify',
    schedule_interval="5 * * * *", #At the 5th minute of every hour
    start_date=datetime(2024,5,16,18),
    catchup=False,
    max_active_runs=1,
    user_defined_macros=MACRO_VARS,
    tags=['spotify-stream']
) as dag:

    initate_dbt_task = BashOperator(
        task_id = 'dbt_initiate',
        bash_command = 'cd /dbt && dbt deps --profiles-dir . --target prod'
    )

    execute_dbt_task = BashOperator(
        task_id = 'dbt_streamify_run',
        bash_command = 'cd /dbt && dbt deps && dbt run --profiles-dir . --target prod'
    )


    staging_table_name = EVENT
    insert_query = f"{{% include 'sql/{EVENT}.sql' %}}" #extra {} for f-strings escape
    external_table_name = f'{staging_table_name}_{EXECUTION_DATETIME_STR}'
    events_data_path = f'{staging_table_name}/month={EXECUTION_MONTH}/day={EXECUTION_DAY}/hour={EXECUTION_HOUR}'
    events_schema = schema[EVENT]
    create_external_table_task = create_external_table(EVENT,
                                                        GCP_PROJECT_ID, 
                                                        BIGQUERY_DATASET, 
                                                        external_table_name, 
                                                        GCP_GCS_BUCKET, 
                                                        events_data_path)
    create_empty_table_task = create_empty_table(EVENT,
                                                    GCP_PROJECT_ID,
                                                    BIGQUERY_DATASET,
                                                    staging_table_name,
                                                    events_schema)
                                            
    execute_insert_query_task = insert_job(EVENT,
                                            insert_query,
                                            BIGQUERY_DATASET,
                                            GCP_PROJECT_ID)
    delete_external_table_task = delete_external_table(EVENT,
                                                        GCP_PROJECT_ID, 
                                                        BIGQUERY_DATASET, 
                                                        external_table_name)
                    
        
    create_external_table_task >> \
    create_empty_table_task >> \
    execute_insert_query_task >> \
    delete_external_table_task >> \
    initate_dbt_task >> \
    execute_dbt_task