import sys; sys.path.append("src") 
from flask import Blueprint

from booter import BasicBooter
from module.interface.manager import manager

from .result import Result

booter = BasicBooter()

control_api = Blueprint('control_api', __name__)

def check_module_can_control(name: str) -> bool:
    # 不是一键控制，也部署 booter 的子模块
    # 目前只有 booter 的子模块可以单独的启动的暂停
    return name == "booter" or name in booter.sub_module_list

@control_api.route("/module/<name>/start", methods=['POST'])
def start(name: str):
    # 验证启动模块请求 
    if not check_module_can_control(name):
        return "module is not found or can't be controlled", 400
        
    if name  == "booter":
        booter.start()
    else:
        booter.start_sub_module(name)

    return "ok", 200
    

@control_api.route("/module/<name>/stop", methods=['POST'])
def stop(name: str):
    if not check_module_can_control(name):
        return "module is not found or can't be controlled", 400
    
    if name == "booter":
        booter.stop()
    else:
        booter.stop_sub_module(name)

    return "ok", 200

@control_api.route("/module/<name>/status", methods=['GET'])
def status(name: str):
    info = manager.info(name)

    if info is None:
        return Result.create(), 404
    
    return Result.create(info={"status": info.status}), 200

@control_api.route("/send/message", methods=['POST'])
def send_message():
    ...