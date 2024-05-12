from flask import Blueprint, request

from message import Message, MessageKind

from server import MANAGER
from .result import Result

interact_api = Blueprint('interact_api', __name__)

@interact_api.route("/interact/message", methods=["POST"])
def send_message():
    data = request.get_json()

    content = data["content"]

    message = Message(MessageKind.Admin, content)

    if MANAGER.module("booter").send(message):
        return Result.create(), 200
    else:
        return Result.create(), 200