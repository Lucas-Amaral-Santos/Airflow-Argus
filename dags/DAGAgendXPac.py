import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd

def merge_agend_pactrat():
    df_pactrat = pd.read_csv('/home/lucas/airflow/input/PAC_TRAT_FILTER.csv', sep=";", encoding="utf8")
    df_pacagend = pd.read_csv('/home/lucas/airflow/input/PAC_TRAT_AGEND.csv', sep=";", encoding="utf8")
    

    df_pactrat.rename(columns={'Nome': 'Atendido'}, inplace=True)
    df_pactrat['Atendido'] = df_pactrat['Atendido'].str.upper()
    df = df_pacagend.merge(df_pactrat, how='inner', on='Atendido')



    df.to_csv('/home/lucas/airflow/PACTRATxAGEND.csv', sep=";")


default_args = {
    'owner': 'lucas',
    'start_date': dt.datetime(2020, 3, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('MergePacTratAgeng', default_args=default_args, schedule_interval=timedelta(minutes=5)) as dag:
    print_starting = BashOperator(task_id='starting', bash_command='echo "I am reading the CSV now....."')

    coping = BashOperator(task_id='coping', bash_command='cp -f /home/lucas/airflow/PAC_TRAT_AGEND.csv /home/lucas/airflow/PAC_TRAT_FILTER.csv /home/lucas/airflow/input/')
    
    CSVJson = PythonOperator(task_id='mergePacTratAgeng', python_callable=merge_agend_pactrat)

print_starting.set_downstream(coping)
coping.set_downstream(CSVJson)