from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook

import requests
import csv
from datetime import datetime

@dag
def user_processing():
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id = "postgres",
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(100),
            username VARCHAR(100),
            email VARCHAR(100) UNIQUE NOT NULL,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    # delete_table = SQLExecuteQueryOperator(
    #     task_id="delete_table",
    #     conn_id = "postgres",
    #     sql = """
    #     DROP TABLE IF EXISTS users;
    #     """
    # )

    @task.sensor(poke_interval=10, timeout=60)
    def is_api_available() -> PokeReturnValue:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        print(response.status_code)

        if response.status_code == 200:
            condition = True
            fake_user = response.json()
        else:
            condition = False
            fake_user = None
        return PokeReturnValue(is_done=condition, xcom_value=fake_user)
    
    @task
    def extract_user(fake_user):
        return {
            "id" : fake_user[0]["id"],
            "name" : fake_user[0]["name"],
            "username" : fake_user[0]["username"],
            "email" : fake_user[0]["email"]
        }
    
    @task
    def process_user(user_data):
        user_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/user_info.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=user_data.keys())
            writer.writeheader()
            writer.writerow(user_data)

    @task
    def store_user():
        hook = PostgresHook(
            postgres_conn_id="postgres"
        )
        hook.copy_expert(
            sql=" COPY users FROM STDIN WITH CSV HEADER",
            filename="/tmp/user_info.csv"
        )

    process_user(extract_user(create_table >> is_api_available())) >> store_user()

user_processing()