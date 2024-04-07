from gensim.models.fasttext import load_facebook_vectors
import redis
import json
import re

# 下载地址：https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.zh.300.bin.gz
# 将下载的文件解压后放在根目录下
# 加载预训练的中文 FastText 模型
print("Loading FastText model...")
model = load_facebook_vectors("cc.zh.300.bin")
print("FastText model loaded.")

# 创建 Redis 连接
print("Connecting to Redis...")
r = redis.Redis(host="localhost", port=6379, db=0)
print("Connected to Redis.")

# 第一步：数据源的收集和整理
# 从本地.json文件获取数据
print("Loading data from local file...")
local_file_path = "data/baidu.json"
with open(local_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 将所有的文档连接成一个长字符串
file_text = " ".join([item["document"] for item in data.values()])

# 第三步：分片
# 将本地文件文本按句子拆分
knowledge_base = re.split("。|！|？", file_text)

for text in knowledge_base:
    # 使用 FastText 模型生成词嵌入
    text_embedding = model[text]

    # 将词嵌入存储在 Redis 中
    r.hset("knowledge_base_embeddings", text, text_embedding.tobytes())

print("Data collection finished.")
