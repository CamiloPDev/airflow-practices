from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@dag
def delete_table_user():
    
    delete_table = SQLExecuteQueryOperator(
        task_id="delete_table",
        conn_id = "postgres",
        sql = """
        DROP TABLE IF EXISTS users;
        """
    )

    delete_table

delete_table_user()