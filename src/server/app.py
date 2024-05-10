import sys; sys.path.append("src") 

from flask import Flask

from server.api import API_LIST
from server.api.result import ResultResponse

from server import ws_server

app = Flask(__name__)

# 注册 API
for api in API_LIST:
    app.register_blueprint(api)

# 自定义返回类型
app.response_class = ResultResponse


def run():
    ws_server.start()
    app.run("0.0.0.0", 8082, debug=False)

if __name__ == '__main__':
    run()