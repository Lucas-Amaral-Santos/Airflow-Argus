import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd

def read_filter_PACTRAT():
    df=pd.read_csv('/home/lucas/airflow/input/b1.csv', sep=";", encoding="utf8")
    # Exclui linhas cuja coluna ÁREA DE ATENDIMENTO em branco
    df = df.dropna(subset=['Área atend'])

    # Copia para um dataframe temporário
    df_limpa = df

    # Fazemos o foward fill nas colunas NOME e CPF 
    cols = ['Nome', 'CPF']
    df_limpa[cols] = df_limpa[cols].ffill()

    # Unimos todas as linhas com mesmo NOME e CPF e concatenamos o a coluna ÁREA DE ATENDIMENTO
    df_limpa = df_limpa.groupby(cols)['Área atend'].apply(' '.join).reset_index()

    # Retira linhas cuja coluna SITUAÇÃO está em branco
    df = df.dropna(subset=['Situação'])

    # Substitui a coluna ÁREA DE ATENDIMENTO já concatenada ao dataframe original
    df['Área atend'] = df_limpa['Área atend']

    df['Cidade'] = df['Cidade/UF'].str.split('/').str[0].copy()
    df['Cidade'] = df['Cidade'].str.title().str.strip() 

    df['Idade'] = df['Idade'].str.extract('(\d+)', expand=False)
    df['Idade'] = df['Idade'].dropna().astype(int)

    df['Entrada'] = pd.to_datetime(df['Entrada'], format="%d/%m/%Y")
    df['Dt Nasc'] = pd.to_datetime(df['Dt Nasc'], format="%d/%m/%Y")

    
    df['CID-10'] = df['CID-10'].str.capitalize().str.slice(start=0, stop=3)

    #  limpando Convênio
    df['Convênio'] = df['Convênio'].str.replace('SIM (oficina-cer)', 'SIM (oficina - cer)')

    # Reinicia o index
    df.index=df.reset_index().index
    df.to_csv('PAC_TRAT_FILTER.csv', sep=";")


default_args = {
    'owner': 'lucas',
    'start_date': dt.datetime(2020, 3, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('ReadPacTrat', default_args=default_args, schedule_interval=timedelta(minutes=5)) as dag:
    print_starting = BashOperator(task_id='starting', bash_command='echo "I am reading the CSV now....."')
    
    CSVJson = PythonOperator(task_id='readPacTrat', python_callable=read_filter_PACTRAT)

print_starting.set_downstream(CSVJson)