from flask import Blueprint

account_api = Blueprint("account_api", __name__)


@account_api.route("/login", methods=["POST"])
def login(): ...


@account_api.route("/admin/add", methods=["POST"])
def add_admin(): ...


@account_api.route("/admin", methods=["DELETE"])
def remote_admin(): ...


@account_api.route("/admin", methods=["PUT"])
def delete_admin(): ...


@account_api.route("/admin/add", methods=["GET"])
def list_admin(): ...
