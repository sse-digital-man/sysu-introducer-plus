from flask import Blueprint

from framework.docker.client import DOCKER_CLIENT
from .result import Result

docker_api = Blueprint("docker_api", __name__)

# @control_api.route("/module/docker/all", methods=["GET"])
# def get_instance_docker():
#     return Result.create(data={"list": MANAGER.docker_list})


@docker_api.route("/docker/container/list", methods=["GET"])
def get_all_docker_container_list():
    return Result.create({"list": DOCKER_CLIENT.docker_info_list})


@docker_api.route(
    "/docker/container/<regex('start|stop'):cmd>/<name>/<kind>", methods=["POST"]
)
def start_docker_container(cmd: str, name: str, kind: str):
    if cmd == "start":
        status = DOCKER_CLIENT.start_module_container(name, kind)
    else:
        status = DOCKER_CLIENT.stop_module_container(name, kind)

    return Result.create(data={"status": status.value})


# def _start_docker(self):
#     docker_info = self._docker.get(self._kind, None)
#     # 如果缺乏 Docker 配置信息 则直接返回
#     if docker_info is None:
#         return

#     status = DOCKER_CLIENT.get_module_container_status(
#         self.name, self.kind, docker_info
#     )

#     if status == DockerContainerStatus.NOT_LOADED:
#         raise error.ModuleRuntimeError(
#             f"module image '{docker_info.tag}' is not loaded"
#         )
#     if status == DockerContainerStatus.NOT_CREATED:
#         DOCKER_CLIENT.create_module_container(self.name, self.kind, docker_info)

#     DOCKER_CLIENT.start_module_container(self.name, self.kind)

# def _stop_docker(self):
#     docker_info = self._docker.get(self._kind, None)
#     # 如果缺乏 Docker 配置信息 则直接返回
#     if docker_info is None:
#         return

#     is_daemon = docker_info.is_daemon
#     if not is_daemon:
#         DOCKER_CLIENT.stop_module_container(self.name, self.kind)
