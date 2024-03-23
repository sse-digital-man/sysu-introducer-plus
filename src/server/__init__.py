from flask import Flask

from server.account import account_api
from server.control import control_api

app = Flask(__name__)
app.register_blueprint(account_api)
app.register_blueprint(control_api)