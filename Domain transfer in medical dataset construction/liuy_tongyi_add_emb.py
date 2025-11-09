### 接着处理数据集  生成自然语言描述的embedding
label_where_key = {
    "disease":"name",
    "drug":"name",
    "food":"name",
    "inspection_means":"name",
    "drug":"name",
    "manufacturer":"name",
    "second_level_departments":"name",
    "symptoms":"name",
    "treatment_plan":"name"
}

graph_path = "medical"

node_label_names = list(label_where_key.keys())

import psycopg
import json
from pgvector.psycopg import register_vector
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import DirectoryLoader
import numpy as np

model_name = "/home/work/liuytest/demo/maidalun1020/bce-embedding-base_v1"
model_kwargs = {'device': 'npu:0'}
encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

def find_real_prompt_from_pg_vector(user_query):
    pg_con = psycopg.connect(
            dbname="postgres",
            host="localhost",
            user="omm",
            password="ZAQ1234@esz",
            port=5432)
     
     
    pg_con.autocommit=True       
    cur = pg_con.cursor()
    register_vector(pg_con)

    embeddings = model.embed_documents(
        [
            user_query
        ]
    )
    embedding = embeddings[0]
    pg_con.execute(f'SET graph_path  = {graph_path};' )
    pg_con.execute('SET hnsw.ef_search = 100;' )
    embedding = np.asarray(embedding)
    datas = []

    prompt = "已知数据库中存在以下数据信息:\n"
    found = False
    for node in node_label_names:
        # pg_con.execute(f'drop  TABLE IF  EXISTS  zyykg_data_{node} cascade') match (n:person) return  n.feature_emd as emb  order by   (emb <#> %s)* -1 desc  LIMIT 1
        data = pg_con.execute(f'match (n:{node}) where (n.feature_emd::vector <#> %s) < -0.5  return  n ,(n.feature_emd::vector <#> %s) as score order by  score asc  LIMIT 5', (embedding,embedding,)).fetchall()
        if len(data)>0:
            found = True
            for data_inrow in data:
                prompt= prompt+f"得分为{data_inrow[1]},label为{data_inrow[0]},的节点\n"  
    if found:
        return prompt 
    else:
        return "" 



key_values = None
with open("tongyi_query_pair_query.json", 'r',encoding="utf-8") as json_file:
    key_values = json.load(json_file) 

new_query_pair_train = []
for row in key_values:
    new_row ={}
    for key,value in row.items():
        user_query = key
        data_prompt = find_real_prompt_from_pg_vector(user_query)
        print(user_query)
        print(data_prompt)
        new_row["instruction"] = data_prompt+"\n" + "请将以下自然语言翻译为对该数据库的Cypher查询:\n"+user_query
        new_row["output"]=value
        new_query_pair_train.append(new_row)
    if len(data_prompt) > 0:
        print("----------------------------------------------------------------------------------------------------")
        print(user_query)
        print(data_prompt)
        print("----------------------------------------------------------------------------------------------------")

with open('new_query_pair_train_tongyi.json', 'w',encoding="utf-8") as json_file:
    json.dump(new_query_pair_train, json_file ,ensure_ascii=False,indent=4)   