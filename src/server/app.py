from flask import Flask, render_template, redirect
from werkzeug.routing import BaseConverter

from module.interface.log import LOGGER

from .ws import WSServer

from .api import API_LIST
from .api.result import ResultResponse

ws_server = WSServer()

# 这部分需要首先进行加载
LOGGER.add_listener("websocket", lambda log: ws_server.send(log.to_json()))

# 0. 创建对象
FOLDER = "../../static"
app = Flask(__name__, static_url_path="", static_folder=FOLDER, template_folder=FOLDER)


# 1. 设置正则转换器
# https://blog.csdn.net/rytyy/article/details/78939507
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter

# 2. 注册 API
for api in API_LIST:
    app.register_blueprint(api)

# 3. 自定义返回类型
app.response_class = ResultResponse


# --- webui 路由设置 --- #


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/<path:name>", methods=["GET", "PUT", "POST"])
def transfer_api(name: str):
    # 设置 307，在重定向后会保留请求方法
    return redirect("/" + name, 307)


def run():
    ws_server.start()
    app.run("0.0.0.0", 8082, debug=False)
