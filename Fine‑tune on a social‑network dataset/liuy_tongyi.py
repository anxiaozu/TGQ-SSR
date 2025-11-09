# 安装 pip install -U dashscope

import json
import os
import dashscope

 

print()

query_pair = []
# 方法一：使用json.dump()函数保存为JSON格式并写入文件
with open('cypher_base_with_limit_skip_query_filter_none.json', 'r') as file:
    cypher_querys = json.load(file)

for query in cypher_querys:
    response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key='sk-8f8adba56edf4a29a185fb57c5808a1e',
    model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages= [
        {"role": "user", "content": "我正在开发一个自然语言转Cypher的接口，但是我没有自然语言描述，你现在是一名Cypher图查询语言专家，你需要将我的Cypher查询语言转换为自然语言描述,使用中文描述,明确返回值所属的变量，只返回描述即可，不需要过多解释，一定要符合人类的自然语言描述习惯、有些查询不需要指明节点的label信息"},
        {"role": "assistant", "content": "好的"},
        {"role": "user", "content": "match (n1:forum)  where n1.title='Album 1 of Hossein Forouhar' return n1.id, n1.\"creationDate\", n1.title"},
        {"role": "assistant", "content": "查找Album 1 of Hossein Forouhar的id,创建日期和他的标题"},
        {"role": "user", "content": "match (n1:forum)-[r1:hastagforum]->(n2:tag)  where n1.title='Wall of Wojciech Ciesla' return n2.id, n2.name"},
        {"role": "assistant", "content": "查找Wall of Wojciech Ciesla的具有的标签信息的id和名称"},
            {"role": "user", "content": query},
    ],
    result_format='message'
    )
    nl_query = response.output.choices[0].message.content
    print(nl_query)
    print(query)
    query_pair.append({nl_query:query})

# 方法一：使用json.dump()函数保存为JSON格式并写入文件
with open("tongyi_query_pair_query.json", "w", encoding="utf-8") as file:
    json.dump(query_pair, file,indent=4,ensure_ascii=False)
