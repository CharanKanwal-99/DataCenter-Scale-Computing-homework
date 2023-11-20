from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from etl_scripts.transform import transform_data
from etl_scripts.extract import extract_data
from etl_scripts.load import load_data
from datetime import datetime





with DAG(dag_id = 'first_dag',
         start_date = datetime(2023,11,1),
         schedule_interval= '@daily')  as dag:
    
    extract = PythonOperator(
        task_id = 'extract',
        python_callable = extract_data,
        provide_context=True
    )

    transform = PythonOperator(task_id='transform',
                               python_callable = transform_data,
                               provide_context=True)


    load = PythonOperator(task_id = 'load',
                          python_callable = load_data,
                          provide_context=True)



    extract >> transform >> load
