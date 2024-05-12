import sys
sys.path.append("./src")
from module.interface.manager import manager

manager.load_modules()

speaker = manager.object("speaker")

speaker.start()
speaker.speak("你好，我是中大校史介绍官中小大，很高兴能为您介绍中大校史。")

# module_dict = manager.info("speaker")
# print(module_dict.to_dict())
