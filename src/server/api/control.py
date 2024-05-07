import sys; sys.path.append("src") 

from typing import Dict
from flask import Blueprint, request

from utils.config import config
from booter import BasicBooter
from module.interface.manager import manager

from .result import Result

booter = BasicBooter()

control_api = Blueprint('control_api', __name__)

def check_module_can_control(name: str) -> bool:
    # 不是一键控制，也部署 booter 的子模块
    # 目前只有 booter 的子模块可以单独的启动的暂停
    return name == "booter" or name in booter.sub_module_list

@control_api.route("/module/start/<name>", methods=['POST'])
def start(name: str):
    # 验证启动模块请求 
    if not check_module_can_control(name):
        return "module is not found or can't be controlled", 400
        
    if name  == "booter":
        booter.start()
    else:
        booter.start_sub_module(name)

    return "ok", 200
    

@control_api.route("/module/stop/<name>", methods=['POST'])
def stop(name: str):
    if not check_module_can_control(name):
        return "module is not found or can't be controlled", 400
    
    if name == "booter":
        booter.stop()
    else:
        booter.stop_sub_module(name)

    return "ok", 200


@control_api.route("/module/change/<name>", methods=['PUT'])
def change_module_kind(name: str):
    data = request.get_json()
    try:
        kind = data["kind"]
    except:
        return Result.create(), 400

    manager.change_module_kind(name, kind)

    return "ok", 200


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

@control_api.route("/module/list/all", methods=['GET'])
def get_all_module():
    return Result.create(data={"list": manager.module_info_list}), 200


@control_api.route("/module/config/<name>", methods=['GET'])
def get_module_config(name: str):
    try:
        config_list = config.get(name)
        # kind_list = list(config_list.keys()) 
        
        return Result.create(data={
            "config": config_list, 
            # "kinds": kind_list
        }), 200
    except KeyError:
        return Result.create(), 404

@control_api.route("/module/config/<name>", methods=['PUT'])
def modify_module_config(name: str):
    data = request.get_json()

    kind = data["kind"]
    info: Dict = data["content"]

    origin = config.get(name, kind).copy()

    try:
        for (key, value) in info.items():
            origin[key] = value
    except KeyError:
        # 出现未知的
        return Result.create(), 400
    
    config.update(origin, name, kind, save=True)

    return Result.create(), 200