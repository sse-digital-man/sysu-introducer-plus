from flask import Blueprint

from booter import Booter

control_api = Blueprint('control_api', __name__)

booter = Booter()

@control_api.route("/start", methods=['PUT'])
def start():
    # 需要指令验证
    ...

@control_api.route("/stop", methods=['PUT'])
def stop():
    ...

@control_api.route("/check/status", methods=['GET'])
def check_status():
    ...

@control_api.route("/send/message", methods=['POST'])
def send_message():
    ...