from flask import Flask

from api.account import account_api
from api.control import control_api
from api.result import ResultResponse
from ws import WSServer
from module.interface.manager import manager

app = Flask(__name__)
app.register_blueprint(account_api)
app.register_blueprint(control_api)
# 自定义返回类型
app.response_class = ResultResponse

ws_server = WSServer()

manager.load_modules()
manager.set_log_callback(lambda log: ws_server.send(log.to_json()))

def run():
    ws_server.start()
    app.run("0.0.0.0", 8082, debug=False)

if __name__ == '__main__':
    run()