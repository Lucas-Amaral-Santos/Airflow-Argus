import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd

def read_filter_Agendamento():
    df = pd.read_csv('/home/lucas/airflow/input/atendimento.csv', sep=";", encoding="utf8")

    df = df.dropna(how='all')
    
    df['Profissional'] = df['Profissional'].replace('(\s*(falta)*\s*n(a|ã|â)o\s(comunicad)(o|a).*)|(\sfalta)|(falta não justificada)|(sem justificativa)|(f$)', 'não comunicada', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(motivo)\s(pessoa\w).*', ' motivos pessoais', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(sem)\s(acompanhante).$', ' sem acompanhante', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(sem)\s(transporte).*', ' sem transporte', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(f(e|é)rias)\s*(do)*\s*(terapeuta)*.*', ' férias do terapeuta', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(paciente)*\s*(com)*\s(atestado).*', ' com atestado', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(febre).*', ' febre', regex=True)
    df['Profissional'] = df['Profissional'].replace('\s*(viagem).*', ' viagem', regex=True)
    df['Profissional'] = df['Profissional'].replace('Justificativa (falta atendido):não comunicada', 'Justificativa (falta atendido): não comunicada')

    df['Setor'] = df[df['Profissional'].str.contains('Justificativa')==False]['Profissional'].apply(lambda st: st[st.find("(")+1:st.find(")")])


    df['Falta'] = df['Observações'].str.contains('Justificativa')
    df['Falta'] = df['Falta'].where(df['Falta']).bfill(limit=1).fillna(0).astype(bool)
    df = df.assign(Justificativa=df['Observações'].mask(df['Observações'].str.contains('Justificativa')==False))
    df['Justificativa'] = df['Justificativa'].bfill(limit=1)
    df = df.dropna(subset=['Hora'])
    df['Justificativa'] = df['Justificativa'].fillna('Atendido')

    df['Convênio OBS'] = df[df['Observações'].str.contains(' - ')==True]['Observações'].apply(lambda st: st[st.find("-")+2:])

    df['Setor OBS'] = df['Observações'].astype(str)
    df['Setor OBS'] = df['Setor OBS'].apply(lambda st: st[:st.find("-")])

    df['Data'] = pd.to_datetime(df['Data'], format="%d/%m/%Y")

    df['Falta'] = df['Falta'].replace(True, 'Falta')
    df['Falta'] = df['Falta'].replace(False, 'Presença')

    df['Turno'] = df['Hora']
    df['Turno AUX'] = df['Turno'].str[0:2].astype(float)
    df['Turno'] = df['Turno AUX'].where(df['Turno AUX']>12,'Manhã')
    df['Turno'] = df['Turno'].where(df['Turno AUX']<17,'Noite')
    df['Turno'].loc[(df["Turno"]!='Noite') & (df["Turno"] != 'Manhã')] = "Tarde"

    df = df.drop(['Turno AUX'], axis=1)

    df.to_csv('/home/lucas/airflow/PAC_TRAT_AGEND.csv', sep=";")


default_args = {
    'owner': 'lucas',
    'start_date': dt.datetime(2020, 3, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('ReadAgend', default_args=default_args, schedule_interval=timedelta(minutes=5)) as dag:
    print_starting = BashOperator(task_id='starting', bash_command='echo "I am reading the CSV now....."')
    
    CSVJson = PythonOperator(task_id='readAgend', python_callable=read_filter_Agendamento)

print_starting.set_downstream(CSVJson)