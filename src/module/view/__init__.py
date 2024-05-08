import sys
sys.path.append("./src/module/view")
from utils.config import config
from EasyAIVtuber import EasyAIVtuber


info = config.get("view", "basic")

# print(info)

view = EasyAIVtuber(info)
