from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchPythonHook
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
import numpy as np
import logging
logger = logging.getLogger(__name__)

import datetime as dt


# operations.append({
#             "nome": row["Nome"],
#             "situacao": row["Situação"],
#             "area_atend": row["Área atend"],
#             "n_pront": row["Nº pront"],
#             "entrada": row["Entrada"],
#             "saida": row["Saída"],
#             "cpf": row["CPF"],
#             "rg": row["RG"],
#             "pcd": row["PCD"],
#             "nis": row["NIS"],
#             "cns": row["CNS"],
#             "dt_nasc": row["Dt Nasc"],
#             "idade": row["Idade"],
#             "sexo": row["Sexo"],
#             "mobilidade": row["Mobilidade"],
#             "diagnostico": row["Diagnóstico"],
#             "cid10": row["CID-10"],
#             "descricao_cid10": row["Descrição CID-10"],
#             "cid11": row["CID-11"],
#             "descricao_cid11": row["Descrição CID-11"],
#             "bnf": row["BNF"],
#             "endereco": row["Endereço"],
#             "bairro": row["Bairro"],
#             "cep": row["Cep"],
#             "cidade_uf": row["Cidade/UF"],
#             "tel_res": row["Tel res"],
#             "tel_rec": row["Tel rec"],
#             "mae": row["Mãe"],
#             "cpf1": row["CPF.1"],
#             "tel_mae": row["Tel mãe"],
#             "tel_pai": row["Tel pai"],
#             "responsavel": row["Responsável"],
#             "cpf3": row["CPF.2"],
#             "tel_resp": row["Tel resp"],
#             "meio_transp": row["Meio transp"],
#             "esc_reg": row["Esc Reg"],
#             "medic": row["Medic"],
#             "alerg": row["Alerg"],
#             "comorbidade": row["Comorbidade"],
#             "convenio": row["Convênio"],
#             "convenio preferencial": row["Convênio Preferencial"],
#             "atividade": row["Atividade"],
#             "uso_imagem": row["Uso imagem"],
#             "obs": row["Obs"],
#             "cidade": row["Cidade"]            
#         })

def generator(df, index):
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

def inject_data_into_es():


    # es_hosts = ["http://localhost:9200"]
    es_hosts = ['https://my-elasticsearch-project-a9672d.es.us-east-1.aws.elastic.cloud:443']
    es_client = Elasticsearch(hosts=es_hosts, 
                            #   http_auth=('elastic', 'SiDFpYX4'),
                              api_key="cU40Y3ZaUUJkMkdDUkVPRERmVlA6dHN0UEY1TjhURWUwZDNhSUJxS1Z4QQ==")
    index = 'pacientes'
    df=pd.read_csv('/home/lucas/airflow/input/PAC_TRAT_FILTER.csv', sep=";")
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

    document = generator(df, index)
    
    resp = es_client.bulk(
        operations=document
    )

    print(resp)
   
    return True

    # action = []
    # for row in json_records:
    #     record = {
    #         'op_time': 'index',
    #         '_index': 'pactrat',
    #         '_source': row
    #     }
    #     action.append(record)

    # df_custom = generator(df)


    # for i,r in df.iterrows():
    #     es_client.index(
    #             index="my_index",
    #             id="my_document_id",
    #             document= {
    #                 "nome": r["Nome"],
    #                 "situacao": r["Situação"],
    #                 "area_atend": r["Área atend"],
    #                 "n_pront": r["Nº pront"],
    #                 "entrada": r["Entrada"],
    #                 "saida": r["Saída"],
    #                 "cpf": r["CPF"],
    #                 "rg": r["RG"],
    #                 "pcd": r["PCD"],
    #                 "nis": r["NIS"],
    #                 "cns": r["CNS"],
    #                 "dt_nasc": r["Dt Nasc"],
    #                 "idade": r["Idade"],
    #                 "sexo": r["Sexo"],
    #                 "mobilidade": r["Mobilidade"],
    #                 "diagnostico": r["Diagnóstico"],
    #                 "cid10": r["CID-10"],
    #                 "descricao_cid10": r["Descrição CID-10"],
    #                 "cid11": r["CID-11"],
    #                 "descricao_cid11": r["Descrição CID-11"],
    #                 "bnf": r["BNF"],
    #                 "endereco": r["Endereço"],
    #                 "bairro": r["Bairro"],
    #                 "cep": r["Cep"],
    #                 "cidade_uf": r["Cidade/UF"],
    #                 "tel_res": r["Tel res"],
    #                 "tel_rec": r["Tel rec"],
    #                 "mae": r["Mãe"],
    #                 "cpf1": r["CPF.1"],
    #                 "tel_mae": r["Tel mãe"],
    #                 "tel_pai": r["Tel pai"],
    #                 "responsavel": r["Responsável"],
    #                 "cpf3": r["CPF.2"],
    #                 "tel_resp": r["Tel resp"],
    #                 "meio_transp": r["Meio transp"],
    #                 "esc_reg": r["Esc Reg"],
    #                 "medic": r["Medic"],
    #                 "alerg": r["Alerg"],
    #                 "comorbidade": r["Comorbidade"],
    #                 "convenio": r["Convênio"],
    #                 "convenio preferencial": r["Convênio Preferencial"],
    #                 "atividade": r["Atividade"],
    #                 "uso_imagem": r["Uso imagem"],
    #                 "obs": r["Obs"],
    #                 "cidade": r["Cidade"],
    #             },
    #     )

        # print(r['Nome'])

    # result = helpers.bulk(es_client, action)
    # print(f"Ingestion completed.")
    # print(result)
    # return True

    
    

    # query = {"query": {"match_all": {}}}
    # result = es_hook.search(query=query)
    # print(es_hook.info())
    # return True


# default_args = {
#     'owner': 'lucas',
#     'start_date': dt.datetime(2025, 1, 25),
#     'retries': 1,
#     'retry_delay': dt.timedelta(minutes=5),
#     'schedule': "@daily",
#     'doc_md': __doc__,
# }

default_args = {
    'owner': 'lucas',
    'start_date': dt.datetime(2020, 3, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG("InsertIntoElastic", default_args=default_args) as dag:
    
    inject_data_into_es_operator = PythonOperator(
        task_id='inject_data_into_es',
        python_callable=inject_data_into_es,
        provide_context=True
    )