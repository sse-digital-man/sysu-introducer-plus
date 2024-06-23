from flask import Blueprint, request

from message import Message, MessageKind
from framework.manager import MANAGER
from .result import Result

interact_api = Blueprint("interact_api", __name__)


@interact_api.route("/interact/message", methods=["POST"])
def send_message():
    data = request.get_json()

    content = data["content"]

    message = Message(MessageKind.Admin, content)

    if MANAGER.send(message):
        return Result.create()

    return Result.create()
