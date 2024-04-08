import json
from elasticsearch import Elasticsearch

# 本地使用Elasticsearch客户端存储历史文件

if __name__ == "__main__":
    es = Elasticsearch(["http://localhost:9200"])
    indexname = "school_library"
    # 先删除索引
    es.indices.delete(index=indexname)
    # 后更新索引
    es.indices.create(index=indexname)

    # 基于数据库建立es索引
    with open("data\database.json", "r", encoding="utf-8") as f:
        _dict = json.load(f)
    for _, dict in _dict.items():
        es.index(index=indexname, body=dict)
