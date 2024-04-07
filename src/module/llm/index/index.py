import json
import os
import time
from elasticsearch import Elasticsearch

# 本地创建Elasticsearch客户端用于存储历史文件
# 首先下载elasticsearch,网站:https://www.elastic.co/cn/downloads/elasticsearch,在安装目录下,在config/elasticsearch.yml将SSL禁用,使用bin/elasticsearch.bat启动
# 参考网站https://stackoverflow.com/questions/71492404/elasticsearch-showing-received-plaintext-http-traffic-on-an-https-channel-in-con


if __name__ == "__main__":
    es = Elasticsearch(["http://localhost:9200"])
    indexname = "school_library"
    # 先删除索引
    es.indices.delete(index=indexname)
    # 后更新索引
    es.indices.create(index=indexname)

    # 基于数据库建立es索引
    with open("src\module\llm\index\database.json", "r", encoding="utf-8") as f:
        _dict = json.load(f)
    for _, dict in _dict.items():
        es.index(index=indexname, body=dict)
