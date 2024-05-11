import sys
sys.path.append("./src")
from module.interface import manager

manager.load_modules()


view = manager.object("view")

view.start()

module_dict = manager.info("view")
print(module_dict.to_dict())