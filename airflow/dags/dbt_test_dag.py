from datetime import datetime

from airflow.operators.bash import BashOperator

from airflow import DAG

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id = 'dbt_test',
    default_args = default_args,
    description = 'Test dbt',
    schedule_interval="@once", #At the 5th minute of every hour
    start_date=datetime(2022,3,20),
    catchup=True,
    tags=['spotify', 'dbt']
) as dag:

    dbt_test_task = BashOperator(
        task_id = "dbt_test",
        bash_command = "cd /dbt && dbt deps --profiles-dir . --target prod"
    )

    dbt_test_task