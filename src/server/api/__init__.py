from .account import account_api
from .control import control_api
from .docker import docker_api
from .interact import interact_api

API_LIST = [account_api, control_api, interact_api, docker_api]
