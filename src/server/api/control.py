from typing import Dict
from flask import Blueprint, request

from module.interface.info import moduleStatusMap
from utils.config import config
from server import manager

from .result import Result, ErrorCode

control_api = Blueprint('control_api', __name__)

booter = manager.object("booter")

def check_module_can_control(name: str) -> bool:
    if manager.object(name) == None:
        return Result.create(code=ErrorCode.ModuleNotFound)
    elif name == "booter" or name in booter.sub_module_list:
        # 目前只有 booter 与其子模块才可以单独地启动的暂停
        return None
    else:
        return Result.create(code=ErrorCode.ModuleUncontrollable)

@control_api.route("/module/<regex('start|stop'):control>/<name>", methods=['POST'])
def start(name: str, control: str):
    # 验证启动模块请求 
    result = check_module_can_control(name)

    if result is not None:
        return result
    
    if control == "start":
        flag, status = booter.start_sub_module(name) \
            if name != "booter" else booter.start()
    elif control == "stop":
        flag, status = booter.stop_sub_module(name) \
            if name != "booter" else booter.stop()
    
    # 如果模块启动失败，则说明是当前状态不支持
    if not flag:
        return Result.create(
            code=ErrorCode.ModuleStatusNotSupported,
            data={ 
                "status": status, 
                "statusLabel": moduleStatusMap[status] 
            })

    return Result.create()

'''
@control_api.route("/module/stop/<name>", methods=['POST'])
def stop(name: str):
    # 验证启动模块请求 
    result = check_module_can_control(name)
    if result is not None:
        return result
    
    if name == "booter":
        booter.stop()
    else:
        booter.stop_sub_module(name)

    return Result.create()
'''

@control_api.route("/module/change/<name>", methods=['PUT'])
def change_module_kind(name: str):
    data = request.get_json()
    try:
        kind = data["kind"]
    except:
        return Result.create(code=ErrorCode.KeyDataMissing)

    manager.change_module_kind(name, kind)

    return Result.create()

@control_api.route("/module/config/<name>", methods=['PUT'])
def modify_module_config(name: str):
    try:
        data = request.get_json()

        kind = data["kind"]
        content: Dict = data["content"]

        config.update(name, kind, content, save=True)
    except BaseException:
        # 出现未知的
        return Result.create()
    

    return Result.create()

'''
@control_api.route("/module/status/<name>", methods=['GET'])
def status(name: str):
    info = manager.info(name)

    if info is None:
        return Result.create(), 404
    
    return Result.create(data={"status": info.status}), 200


@control_api.route("/module/info/<name>", methods=['GET'])
def get_single_module(name: str):
    info = manager.info(name)

    if info is None:
        return Result.create(), 404
    
    return Result.create(data={"info": info.to_dict()}), 200

@control_api.route("/module/list/controllable", methods=['GET'])
def get_controllable_module():
    with_booter = request.args.get("withBooter") not in [0, None]

    infos = [manager.info(sub_module) for sub_module in booter.sub_module_list]
    
    if with_booter:
        infos.append(booter.info)

    result = []

    for info in infos:    
        result.append(info.to_dict())

    return Result.create(data={"list": result}), 200
'''

@control_api.route("/module/list/all", methods=['GET'])
def get_all_module():
    return Result.create(data={"list": manager.module_info_list})

@control_api.route("/module/config/<name>", methods=['GET'])
def get_module_config(name: str):
    try:
        config_list = config.get(name)
        # kind_list = list(config_list.keys()) 
        
        return Result.create(data={
            "config": config_list, 
            # "kinds": kind_list
        })
    except KeyError:
        return Result.create(code=ErrorCode.ModuleConfigEmpty)
