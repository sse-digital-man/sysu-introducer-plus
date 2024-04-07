from elasticsearch import Elasticsearch
from bot.gpt import GPTBot

def data_retrieve(p_query):
    es = Elasticsearch(["http://localhost:9200"])
    indexname = "school_library"

    # 查询语句
    dsl = {"query": {"match": {"metadata": p_query}}, "size": 5}
    res = es.search(index=indexname, body=dsl)
    simQ_list = []

    # 遍历得到前5个相似问题
    for doc in res["hits"]["hits"]:
        _metadata = doc["_source"]["metadata"]
        _document = doc["_source"]["document"]
        simQ_list.append(_metadata + ":" + _document)
        print(_metadata + ":" + _document)
    return simQ_list


if __name__ == "__main__":
    bot = GPTBot()
    user_input = input("请输入语句：")

    p_query = "你好,能帮助将问题的关键词出来吗？下面是示例:Q:请问一下中山大学在2024年发生了什么? A:中山大学,校史,2024年"
    response = bot._single_call(p_query + user_input)
    print(response)