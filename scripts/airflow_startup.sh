#!/bin/bash
echo "Changing permissions for dbt folder..."
cd ~/spotify_data_pipeline/ && sudo chmod -R 777 dbt

echo "Building airflow docker images..."
cd ~/spotify_data_pipeline/airflow
docker-compose build

echo "Running airflow-init..."
docker-compose up airflow-init

echo "Starting up airflow in detached mode..."
docker-compose up -d

echo "Airflow started successfully."
echo "Airflow is running in detached mode. "
echo "Run 'docker-compose logs --follow' to see the logs."