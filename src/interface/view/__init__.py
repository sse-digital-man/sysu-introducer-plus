import sys
sys.path.append("./src/interface/view")
from utils.config import config
from EasyAIVtuber import EasyAIVtuber


info = config.get_use_interface("view")

# print(info)

view = EasyAIVtuber(info)
