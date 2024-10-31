from datetime import datetime
from airflow import DAG
from airflow.providers.trino.operators.trino import TrinoOperator
from airflow.operators.python_operator import PythonOperator

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 17),
    'retries': 1, # cho phép thử lại task khi thất bại, ở đây đang để 1 lần nếu thất bại
}

# Define the function for the other Python tasks
def print_start():
    print("Start of DAG execution")

def print_end():
    print("End of DAG execution")

# Define the DAG
with DAG(
    'query_dag_ivy',
    default_args=default_args,
    description='A DAG that runs a Trino query',
    schedule_interval='@daily', # Lên lịch cho DAG, ở đây đang để hour
    catchup=False,
) as dag:

    # Python task: Start
    start_task = PythonOperator(
        task_id='print_start',
        python_callable=print_start,
    )

    # Trino task: Execute a SQL query on Trino
    query_task = TrinoOperator(
        task_id='insert_data_inc',
        sql="insert into hive.ivy.customer select *  from sqlserver.dbo.customer WHERE date = CAST('2023-11-25' AS DATE)",  # Replace with your Trino SQL query
        trino_conn_id='my_trino_connection',  # Replace with your Trino connection ID
    )

    # Python task: End
    end_task = PythonOperator(
        task_id='print_end',
        python_callable=print_end,
    )

    # Define task dependencies
    start_task >> query_task >> end_task
