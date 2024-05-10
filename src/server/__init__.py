from flask import Flask, render_template, redirect

from module.interface.manager import manager
from ws import WSServer

from api import API_LIST
from api.result import ResultResponse

ws_server = WSServer()

manager.load_modules()
manager.set_log_callback(lambda log: ws_server.send(log.to_json()))

app = Flask(__name__, static_url_path="", static_folder='../../static', template_folder='../../static')

# 注册 API
for api in API_LIST:
    app.register_blueprint(api)

# 自定义返回类型
app.response_class = ResultResponse

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/<path:name>', methods=["GET", "PUT", "POST"])
def api(name: str):
    # 设置 307，在重定向后会保留请求方法
    return redirect("/" + name, 307)