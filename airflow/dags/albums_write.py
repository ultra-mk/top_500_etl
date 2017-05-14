import albums
import boto3
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


def write_album_frame():
    a = albums.Albums()
    return a.df.to_csv('airflow/dags/csvs/album_frame.csv')


dag = DAG('albums', default_args=default_args, schedule_interval=None)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = PythonOperator(
    task_id='write_album_frame',
    python_callable=write_album_frame,
    dag=dag)

# t2 = BashOperator(
#     task_id='sleep',
#     bash_command='sleep 5',
#     retries=3,
#     dag=dag)

# templated_command = """
#     {% for i in range(5) %}
#         echo "{{ ds }}"
#         echo "{{ macros.ds_add(ds, 7)}}"
#         echo "{{ params.my_param }}"
#     {% endfor %}
# """

# t3 = BashOperator(
#     task_id='templated',
#     bash_command=templated_command,
#     params={'my_param': 'Parameter I passed in'},
#     dag=dag)

# t2.set_upstream(t1)
# t3.set_upstream(t1)