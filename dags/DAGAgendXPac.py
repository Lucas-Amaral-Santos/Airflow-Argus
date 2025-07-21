import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
from slugify import slugify


def merge_agend_pactrat():
    df_pactrat = pd.read_csv('/home/afr/airflow/input/PAC_TRAT_FILTER.csv', sep=";", encoding="utf8")
    df_pacagend = pd.read_csv('/home/afr/airflow/input/PAC_TRAT_AGEND.csv', sep=";", encoding="utf8")


    df_pactrat.rename(columns={'Nome': 'Atendido'}, inplace=True)
    df_pactrat['Atendido'] = df_pactrat['Atendido'].str.upper()
    df = df_pacagend.merge(df_pactrat, how='inner', on='Atendido')

    df['Observações'] = df['Observações'].fillna('')
    df['Avaliação'] = df['Observações'].str.contains('AVALIAÇÃO')
    df['Triagem'] = df['Observações'].str.contains('TRIAGEM')
    df['Oficina'] = df['Observações'].str.contains('OFICINA')

    df['Nulo'] = df['Observações'].isna()==True
    df['Avaliação'] = df['Observações'].str.contains('AVALIAÇÃO' or 'AVALIACAO')
    df['Triagem'] = df['Observações'].str.contains('TRIAGEM')
    df['Oficina'] = df['Observações'].str.contains('OFICINA')
    df['Consulta'] = df['Observações'].str.contains('CONSULTA MEDICA' or 'CONSULTA MÉDICA')

    df['Nulo'] = df['Observações'].isna()==False
    df['Triagem'] = df['Triagem'].fillna(False)
    df['Avaliação'] = df['Avaliação'].fillna(False)
    df['Oficina'] = df['Oficina'].fillna(False)
    df['Consulta'] = df['Consulta'].fillna(False)


    df['Tipo'] = 'Tratamento'
    df['Tipo'] = df['Tipo'].where(~df['Nulo'], 'NI')
    df['Tipo'] = df['Tipo'].where(~df['Falta'].str.contains('Falta'), 'Falta')
    df['Tipo'] = df['Tipo'].where(~df['Triagem'], 'Triagem')
    df['Tipo'] = df['Tipo'].where(~df['Consulta'], 'Consulta Médica')
    df['Tipo'] = df['Tipo'].where(~df['Avaliação'], 'Avaliação')
    df['Tipo'] = df['Tipo'].where(~df['Oficina'], 'Oficina')

    df['Oficina'] = df['Convênio.1'].str.match('oficina-cer' or 'oficina-ep' or 'hospital da criança')

    df = df[['Data', 'Hora', 'Profissional',
       'Nº prontuário', 'Atendido', 'Observações', 'Setor', 'Falta',
       'Motivo Just', 'Desc Just', 'Convênio OBS', 'Setor OBS', 'Turno', 'Tipo',
       'Situação', 'Área atend', 'Nº pront', 'Entrada', 'Saída', 'CPF',
       'PCD', 'Dt Nasc', 'Idade', 'Sexo', 'Mobilidade',
       'Diagnóstico', 'CID-10', 'Descrição CID-10', 'CID-11',
       'Descrição CID-11', 'Endereço', 'Bairro', 'Cep',
       'Cidade/UF', 'Mãe', 'Pai', 'Responsável', 'Meio transp',
       'Esc Reg', 'Medic', 'Alerg', 'Comorbidade', 'Convênio', 'Convênio.1',
       'Atividade', 'Uso imagem', 'Obs', 'Cidade', 'Periodo', 'Tipo', 'Oficina']]

    df.to_csv('/home/afr/airflow/PACTRATxAGEND.csv', sep=";")
    df.columns = df.columns.map(lambda x: slugify(x, separator='_'))
	
    df.to_excel("/home/afr/airflow/PACTRATxAGEND.xlsx")
    df.to_csv('/home/afr/airflow/PACTRATxAGEND_BD.csv', sep=";")

default_args = {
    'owner': 'lucas',
    'start_date': dt.datetime(2020, 3, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('MergePacTratAgeng', default_args=default_args, schedule_interval=timedelta(minutes=5)) as dag:
    print_starting = BashOperator(task_id='starting', bash_command='echo "I am reading the CSV now....."')

    coping = BashOperator(task_id='coping', bash_command='cp -f /home/afr/airflow/PAC_TRAT_AGEND.csv /home/afr/airflow/PAC_TRAT_FILTER.csv /home/afr/airflow/input/')
    
    CSVJson = PythonOperator(task_id='mergePacTratAgeng', python_callable=merge_agend_pactrat)

print_starting.set_downstream(coping)
coping.set_downstream(CSVJson)
