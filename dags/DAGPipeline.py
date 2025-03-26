import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchPythonHook
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import numpy as np



def generator_pactrat_agend(df, index):
    indice = {
            "index": {
                "_index": index
            }
        }

    operations = []
    for row in df.iterrows():
        operations.append(indice)
        operations.append({
            "data": str(row[1]["Data"]),
            "hora": str(row[1]["Hora"]),
            "profissional": str(row[1]["Profissional"]),
            "n_prontuario": str(row[1]["Nº prontuário"]),
            "atendido": str(row[1]["Atendido"]),
            "observacoes": str(row[1]["Observações"]),
            "setor": str(row[1]["Setor"]),
            "falta": str(row[1]["Falta"]),
            "justificativa": str(row[1]["Justificativa"]),
            "situacao": str(row[1]["Situação"]),
            "area_atend": str(row[1]["Área atend"]),
            "n_pront": str(row[1]["Nº pront"]),
            "entrada": str(row[1]["Entrada"]),
            "saida": str(row[1]["Saída"]),
            "cpf": str(row[1]["CPF"]),
            "rg": str(row[1]["RG"]),
            "pcd": str(row[1]["PCD"]),
            "nis": str(row[1]["NIS"]),
            "cns": str(row[1]["CNS"]),
            "dt_nasc": str(row[1]["Dt Nasc"]),
            "idade": str(row[1]["Idade"]),
            "sexo": str(row[1]["Sexo"]),
            "mobilidade": str(row[1]["Mobilidade"]),
            "diagnostico": str(row[1]["Diagnóstico"]),
            "cid10": str(row[1]["CID-10"]),
            "descricao_cid10": str(row[1]["Descrição CID-10"]),
            "cid11": str(row[1]["CID-11"]),
            "descricao_cid11": str(row[1]["Descrição CID-11"]),
            "bnf": str(row[1]["BNF"]),
            "endereco": str(row[1]["Endereço"]),
            "bairro": str(row[1]["Bairro"]),
            "cep": str(row[1]["Cep"]),
            "cidade_uf": str(row[1]["Cidade/UF"]),
            "tel_res": str(row[1]["Tel res"]),
            "tel_rec": str(row[1]["Tel rec"]),
            "mae": str(row[1]["Mãe"]),
            "cpf1": str(row[1]["CPF.1"]),
            "tel_mae": str(row[1]["Tel mãe"]),
            "tel_pai": str(row[1]["Tel pai"]),
            "responsavel": str(row[1]["Responsável"]),
            "cpf3": str(row[1]["CPF.2"]),
            "tel_resp": str(row[1]["Tel resp"]),
            "meio_transp": str(row[1]["Meio transp"]),
            "esc_reg": str(row[1]["Esc Reg"]),
            "medic": str(row[1]["Medic"]),
            "alerg": str(row[1]["Alerg"]),
            "comorbidade": str(row[1]["Comorbidade"]),
            "convenio": str(row[1]["Convênio"]),
            "convenio preferencial": str(row[1]["Convênio Preferencial"]),
            "atividade": str(row[1]["Atividade"]),
            "uso_imagem": str(row[1]["Uso imagem"]),
            "obs": str(row[1]["Obs"]),
            "cidade": str(row[1]["Cidade"])            
        })

    return operations

def inject_pactrat_agend_into_es():


    es_hosts = ["http://localhost:9200"]
    es_client = Elasticsearch(hosts=es_hosts, http_auth=('elastic', 'SiDFpYX4'),)
    index = 'pacientes_agendamento'
    df=pd.read_csv('/home/lucas/airflow/input/PACTRATxAGEND.csv', sep=";", on_bad_lines='skip')
    df = df[df['Data'].notna()]
    df = df.replace(np.nan, '')
    df = df.fillna('')

    
    try:
        resp = es_client.indices.delete(
            index=index,
        )
    except:
        pass

    resp = es_client.indices.create(
        index=index,
    )
    print(resp)

    document = generator_pactrat_agend(df, index)
    
    resp = es_client.bulk(
        operations=document
    )

    print(resp)
   
    return True

def generator_pactrat(df, index):
    indice = {
            "index": {
                "_index": index
            }
        }

    operations = []
    for row in df.iterrows():
        operations.append(indice)
        operations.append({
            "nome": str(row[1]["Nome"]),
            "situacao": str(row[1]["Situação"]),
            "area_atend": str(row[1]["Área atend"]),
            "n_pront": str(row[1]["Nº pront"]),
            "entrada": str(row[1]["Entrada"]),
            "saida": str(row[1]["Saída"]),
            "cpf": str(row[1]["CPF"]),
            "rg": str(row[1]["RG"]),
            "pcd": str(row[1]["PCD"]),
            "nis": str(row[1]["NIS"]),
            "cns": str(row[1]["CNS"]),
            "dt_nasc": str(row[1]["Dt Nasc"]),
            "idade": str(row[1]["Idade"]),
            "sexo": str(row[1]["Sexo"]),
            "mobilidade": str(row[1]["Mobilidade"]),
            "diagnostico": str(row[1]["Diagnóstico"]),
            "cid10": str(row[1]["CID-10"]),
            "descricao_cid10": str(row[1]["Descrição CID-10"]),
            "cid11": str(row[1]["CID-11"]),
            "descricao_cid11": str(row[1]["Descrição CID-11"]),
            "bnf": str(row[1]["BNF"]),
            "endereco": str(row[1]["Endereço"]),
            "bairro": str(row[1]["Bairro"]),
            "cep": str(row[1]["Cep"]),
            "cidade_uf": str(row[1]["Cidade/UF"]),
            "tel_res": str(row[1]["Tel res"]),
            "tel_rec": str(row[1]["Tel rec"]),
            "mae": str(row[1]["Mãe"]),
            "cpf1": str(row[1]["CPF.1"]),
            "tel_mae": str(row[1]["Tel mãe"]),
            "tel_pai": str(row[1]["Tel pai"]),
            "responsavel": str(row[1]["Responsável"]),
            "cpf3": str(row[1]["CPF.2"]),
            "tel_resp": str(row[1]["Tel resp"]),
            "meio_transp": str(row[1]["Meio transp"]),
            "esc_reg": str(row[1]["Esc Reg"]),
            "medic": str(row[1]["Medic"]),
            "alerg": str(row[1]["Alerg"]),
            "comorbidade": str(row[1]["Comorbidade"]),
            "convenio": str(row[1]["Convênio"]),
            "convenio preferencial": str(row[1]["Convênio Preferencial"]),
            "atividade": str(row[1]["Atividade"]),
            "uso_imagem": str(row[1]["Uso imagem"]),
            "obs": str(row[1]["Obs"]),
            "cidade": str(row[1]["Cidade"])            
        })

    return operations

def inject_pactrat_into_es():


    es_hosts = ["http://localhost:9200"]
    es_client = Elasticsearch(hosts=es_hosts, http_auth=('elastic', 'SiDFpYX4'),)
    index = 'pacientes'
    df=pd.read_csv('/home/lucas/airflow/input/PAC_TRAT_FILTER.csv', sep=";", on_bad_lines='skip')
    df = df.replace(np.nan, '')
    df = df.fillna('')

    
    try:
        resp = es_client.indices.delete(
            index=index,
        )
    except:
        pass

    resp = es_client.indices.create(
        index=index,
    )
    print(resp)

    document = generator_pactrat(df, index)
    
    resp = es_client.bulk(
        operations=document
    )

    print(resp)
   
    return True

def merge_agend_pactrat():
    df_pactrat = pd.read_csv('/home/lucas/airflow/input/PAC_TRAT_FILTER.csv', sep=";", encoding="utf8")
    df_pacagend = pd.read_csv('/home/lucas/airflow/input/PAC_TRAT_AGEND.csv', sep=";", encoding="utf8")
    

    df_pactrat.rename(columns={'Nome': 'Atendido'}, inplace=True)
    df_pactrat['Atendido'] = df_pactrat['Atendido'].str.upper()
    df = df_pacagend.merge(df_pactrat, how='inner', on='Atendido')



    df.to_csv('PACTRATxAGEND.csv', sep=";")

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

def read_filter_Agendamento():
    df = pd.read_csv('/home/lucas/airflow/input/atendimento.csv', sep=";", encoding="utf8")
    

    df['Data'] = pd.to_datetime(df['Data'], format="%m/%d/%Y", errors='coerce')

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

    df['Falta'] = df.Profissional.str.contains('Justificativa')
    df['Falta'] = df['Falta'].where(df['Falta']).bfill(limit=1).fillna(0).astype(bool)
    df = df.assign(Justificativa=df['Profissional'].mask(df.Profissional.str.contains('Justificativa')==False))
    df['Justificativa'] = df['Justificativa'].bfill(limit=1)
    df = df.dropna(subset=['Hora']).reset_index().drop(['index'], axis=1)


    df.to_csv('PAC_TRAT_AGEND.csv', sep=";")

default_args = {
    'owner': 'lucas',
    'start_date': dt.datetime(2025, 1, 29),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}



with DAG('PipelineARGUS', default_args=default_args, schedule_interval=timedelta(minutes=5)) as dag:

    selenium_pactrat = BashOperator(task_id='selenium_pactrat', bash_command='Selenium JOB....."')
    selenium_agend = BashOperator(task_id='selenium_agens', bash_command='Selenium JOB....."')


    filterpactrat = PythonOperator(task_id='readPacTrat', python_callable=read_filter_PACTRAT)

    filterpactratagend = PythonOperator(task_id='readAgend', python_callable=read_filter_Agendamento)

    copytoinputdir = BashOperator(task_id='coping', bash_command='cp -f /home/lucas/airflow/PAC_TRAT_AGEND.csv /home/lucas/airflow/PAC_TRAT_FILTER.csv /home/lucas/airflow/input/')

    mergepactratagend = PythonOperator(task_id='mergePacTratAgeng', python_callable=merge_agend_pactrat)

    inject_pactrat_into_es_operator = PythonOperator(
        task_id='inject_pactrat_into_es',
        python_callable=inject_pactrat_into_es,
        provide_context=True
    )

    inject_pactrat_agend_into_es_operator = PythonOperator(
        task_id='inject_pactrat_agend_into_es',
        python_callable=inject_pactrat_agend_into_es,
        provide_context=True
    )

selenium_pactrat.set_downstream(filterpactrat)
selenium_agend.set_downstream(filterpactratagend)

filterpactratagend.set_downstream(copytoinputdir)
filterpactrat.set_downstream(copytoinputdir)


copytoinputdir.set_downstream(mergepactratagend)


mergepactratagend.set_downstream([inject_pactrat_into_es_operator, inject_pactrat_agend_into_es_operator])
