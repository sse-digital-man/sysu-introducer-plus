from booter import BasicBooter
from module.interface.manager import manager

booter = BasicBooter()

# Notice: 需要再运行时统一加载完模块
manager.load_modules()
