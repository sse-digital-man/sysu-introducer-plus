import sys
sys.path.append("./src")
from module.interface.manager import manager

manager.load_modules()

speaker = manager.object("speaker")

speaker.start()
speaker.speak("你好世界")

module_dict = manager.info("speaker")
print(module_dict.to_dict())
