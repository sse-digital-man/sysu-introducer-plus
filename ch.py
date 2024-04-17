import chromadb
import json
from gensim.models.fasttext import load_facebook_vectors

chroma_client = chromadb.Client()
# 集合名字为tizi365
collection = chroma_client.create_collection(name="tizi365")
# 添加2条文本数据，通过embeddings参数指定每条文本数据的向量
# 这种方式适合我们自己选择文本嵌入模型，提前计算出文本向量

model = load_facebook_vectors("cc.zh.300.bin")
# 读取 JSON 文件
with open("data/database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []
metadatas = []

# 遍历 JSON 数据
for key, value in data.items():
    # 添加文档到相应的列表
    documents.append(value["document"])

    # 将元数据字符串转换为字典
    metadata_str = value["metadata"]
    metadata_dict = {key: True for key in metadata_str.split(",")}

    # 添加元数据字典到相应的列表
    metadatas.append(metadata_dict)


# 打印结果
# print("Documents:", documents)
# print("Metadatas:", metadatas)

embeddings = [model.get_vector(text).tolist() for text in documents]


collection.add(
    embeddings=embeddings,
    documents=documents,
    metadatas=metadatas,
    ids=[str(i) for i in range(len(documents))],
)

# 设置一个开始的时间
# 用于计算查询时间
import time

start = time.time()
query = "中山大学的校史。"
query_embedding = model.get_vector(query).tolist()
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
)

print(results)
# 打印查询时间
print("Query time:", time.time() - start)
