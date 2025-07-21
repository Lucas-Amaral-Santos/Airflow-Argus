import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import numpy as np
import regex

def read_filter_Agendamento():
    df=pd.read_excel('/home/afr/airflow/input/atendimento.xlsx', skiprows=1, skipfooter=1)
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

    df['Motivo Justificativa'] = df['Justificativa'].str.split(': ', expand=True)[1]
    df['Motivo Justificativa'] = df['Motivo Justificativa'].fillna('Não faltou')

    df['Tipo Falta'] = df['Justificativa'].str.split(': ', expand=True)[0]
    df['Tipo Falta'] = df['Tipo Falta'].str.replace('Justificativa (falta atendido)', 'Paciente', regex=False)
    df['Tipo Falta'] = df['Tipo Falta'].str.replace('Justificativa (falta profissional)', 'Profissional', regex=False)
    df['Tipo Falta'] = df['Tipo Falta'].str.replace('Justificativa (falta )', 'Não informado', regex=False)

    df['Turno'] = df['Hora']
    df['Turno AUX'] = df['Turno'].astype(str).str[0:2].astype(float)
    df['Turno'] = df['Turno AUX'].where(df['Turno AUX']>=12,'Manhã')
    df['Turno'] = df['Turno'].where(df['Turno AUX']<18,'Noite')
    df['Turno'].loc[(df["Turno"]!='Noite') & (df["Turno"] != 'Manhã')] = "Tarde"

    df = df.drop(['Turno AUX'], axis=1)

    df['Justificativa'] = df['Motivo Justificativa'].str.split('-', expand=True)[0]

    df['Desc Justificativa'] = df['Motivo Justificativa'].str.split('-', expand=True)[1]
    df['Desc Justificativa'].fillna('Não informado', inplace=True)
    

    fono_errado     = df[df['Setor OBS'].str.contains('FONO')]['Setor OBS'].unique()
    fisio_errado    = df[df['Setor OBS'].str.contains('FISIOTERAPIA GERA|FISIOTERAPI GERA')]['Setor OBS'].unique()
    psigera_errado  = df[df['Setor OBS'].str.contains('PSICOLOGIA GERA|PSICOLOGI GERA')]['Setor OBS'].unique()
    pilates_errado  = df[df['Setor OBS'].str.contains('PILATES')]['Setor OBS'].unique()
    fisiresp_errado = df[df['Setor OBS'].str.contains('RESP')]['Setor OBS'].unique()
    fisiped_errado  = df[df['Setor OBS'].str.contains('PED')]['Setor OBS'].unique()
    fisipel_errado  = df[df['Setor OBS'].str.contains('PÉL')]['Setor OBS'].unique()
    reint_errado    = df[df['Setor OBS'].str.contains('REINT')]['Setor OBS'].unique()
    terocu_errado   = df[df['Setor OBS'].str.contains('OCUP')]['Setor OBS'].unique()

    eletro_errado   = df[df['Setor OBS'].str.contains('ELETROT')]['Setor OBS'].unique()
    eletro_errado   = np.append(eletro_errado, ['TENS', 'TENS ', 'ULTRASSOM', 'ULTRASSOM ', 'ULTRA SOM', 'ULTRA SOM ', 'MICRO ONDAS', 'FORNO DE BIER', 'ONDAS CURTAS', 'INFRA VERMELHO', 'MICRO ONDAS ', 'FORNO DE BIER ', 'ONDAS CURTAS ', 'INFRA VERMELHO '])
    eletro_errado

    motor_errado    = df[df['Setor OBS'].str.contains('MOTOR')]['Setor OBS'].unique()

    massot_errado   = df[df['Setor OBS'].str.contains('MASSOT')]['Setor OBS'].unique()

    fono = 'FONOAUDIOLOGIA GERAL'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=fono_errado,value=fono)

    fisio = 'FISIOTERAPIA GERAL'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=fisio_errado,value=fisio)

    psi_gera = 'PSICOLOGIA GERAL'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=psigera_errado,value=psi_gera)

    pilates = 'PILATES'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=pilates_errado,value=pilates)

    fisiresp = 'FISIOTERAPIA RESPIRATÓRIA'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=fisiresp_errado,value=fisiresp)

    fisiped = 'FISIOTERAPIA PEDIÁTRICA'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=fisiped_errado,value=fisiped)

    fisipel = 'FISIOTERAPIA PÉLVICA'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=fisipel_errado,value=fisipel)

    reint = 'REINTEGRAR'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=reint_errado, value=reint)

    terocu = 'TERAPIA OCUPACIONAL'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=terocu_errado ,value=terocu)

    eletro = 'ELETROTERAPIA'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=eletro_errado ,value=eletro)

    motor = 'FISIOTERAPIA MOTORA'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=motor_errado ,value=motor)

    psi_ni = 'PSICOLOGIA NI'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=['PSICOLOGIA N', 'PSICOLOGIA NI '] ,value=psi_ni)

    psi_ti = 'PSICOLOGIA TI'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=['PSICOLOGIA T', 'PSICOLOGIA TI '] ,value=psi_ti)

    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=['PSICOLOGI', 'PSICOLOGIA', 'PSICOLOGIA '] ,value='PSICOLOGIA')

    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=['FISIOTERAPI ', 'FISIOTERAPI'] ,value='FISIOTERAPIA')


    massot = 'MASSOTERAPIA'
    df['Setor OBS'] = df['Setor OBS'].replace(to_replace=massot_errado ,value=massot)

    df['Justificativa'] = df['Justificativa'].str.replace('falta comunicada. paciente antecipou a aula para dia 26/06/25','mudança de horário')
    df['Justificativa'] = df['Justificativa'].str.replace('falta comunicada. paciente antecipou a aula para dia 26/06/25 ','mudança de horário')
    df['Justificativa'] = df['Justificativa'].str.replace('o serviã§o social, comunicou que o responsã¡vel solicitou alta dos atendimentos.','alta do setor')
    df['Justificativa'] = df['Justificativa'].str.replace('o serviã§o social, comunicou que o responsã¡vel solicitou alta dos atendimentos. ','alta do setor')

    ncom_errado = df[df['Justificativa'].str.contains('comuni')]['Justificativa'].unique()
    ncom = 'não comunicada'
    df['Justificativa'] = df['Justificativa'].replace(to_replace=ncom_errado ,value=ncom)


    doen_errado = df[df['Justificativa'].str.contains('doen')]['Justificativa'].unique()

    doen = 'doença'
    df['Justificativa'] = df['Justificativa'].replace(to_replace=doen_errado ,value=doen)

    pess_errado = df[df['Justificativa'].str.contains('pess')]['Justificativa'].unique()

    pess = 'motivo pessoal'
    df['Justificativa'] = df['Justificativa'].replace(to_replace=pess_errado ,value=pess)

    df.drop(['Motivo Justificativa'], axis=1, inplace=True)

    df.rename(columns={'Setor':'Profissão'}, inplace=True)

    pattern = r'\((?:[^()]+|(?R))*\)'

    df['Profissional'] = df['Profissional'].apply(lambda x: regex.sub(pattern, '', x))


    df.to_csv('/home/afr/airflow/PAC_TRAT_AGEND.csv', sep=";")


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
