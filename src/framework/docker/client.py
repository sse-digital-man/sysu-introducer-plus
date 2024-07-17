import sys
from typing import List, Dict, Any

import docker
import docker.errors
import docker.types

from .info import DockerContainerStatus
from .load import load_docker_config

from ..info import to_instance_label as to_container_name

# Macos Docker 启动配置
# socat TCP-LISTEN:2375,reuseaddr,fork UNIX-CONNECT:/var/run/docker.sock &

HOST = "127.0.0.1"
PORT = 2375

RUNNING = "running"

DOCKER_PATH = "conf/docker.yaml"


def generate_url(host: str, port: int):
    return f"tcp://{host}:{port}"


class DockerClient:
    def __init__(self):
        self._client = docker.DockerClient(base_url=generate_url(HOST, PORT))

    # 验证image 是否存在
    def check_image(self, name: str) -> bool:
        """验证 image 是否存在

        Args:
            name (str): 镜像对应的名称，格式: name:version

        Returns:
            bool: 是否存在
        """
        try:
            self._client.images.get(name)
            return True
        except docker.errors.ImageNotFound:
            return False

    def create_container(self, name: str, kwargs: dict):
        # 端口映射: https://www.jianshu.com/p/c1bfc14d5c02
        # 环境变量: https://stackoverflow.com/questions/67482434/set-environment-var-to-docker-container-created-in-python

        # 如果容器存在则直接返回
        if self.check_container(name):
            return False

        self._client.containers.create(**kwargs)

        return True

    # 验证容器是否存在
    def check_container(self, name: str) -> bool:
        # self._client.containers÷
        try:
            self._client.containers.get(name)
            return True
        except docker.errors.NotFound:
            return False

    # 启动容器
    def start_container(self, name: str):
        self._get_container(name).start()

    # 关闭容器
    def stop_container(self, name: str):
        self._get_container(name).stop()

    def _get_container(self, name: str) -> Any | None:
        try:
            return self._client.containers.get(name)
        except docker.errors.NotFound:
            return None

    def get_container_status(self, name: str) -> DockerContainerStatus:
        if not self.check_container(name):
            return DockerContainerStatus.NOT_CREATED

        status = self._get_container(name).status
        if status == "running":
            return DockerContainerStatus.RUNNING
        elif status == "exited":
            return DockerContainerStatus.EXITED

        return DockerContainerStatus.NOT_CREATED


class ModuleDockerClient:
    def __init__(self):
        self.__client = DockerClient()
        self.__info_dict = load_docker_config(DOCKER_PATH)

    def create_module_container(
        self,
        name: str,
        kind: str,
    ):
        """创建模块容器

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型
        """
        container_name = to_container_name(name, kind)

        self.__client.create_container(container_name, self.__info_dict[container_name])

    def start_module_container(
        self, name: str, kind: str, auto_create: bool = True
    ) -> DockerContainerStatus:
        """启动模块容器

        Args:
            name (str): 模块名称
            kind (str): 模块试下类型
            auto_create (bool, optional): 是否自动创建. Defaults to True.

        Raises:
            FileNotFoundError: 模块容器不存在

        Returns:
            DockerContainerStatus: 返回当前容器状态
        """
        container = to_container_name(name, kind)

        info = self.__info_dict.get(container)
        if info is None:
            raise FileNotFoundError(f"instance '{container}' doesn't have docker")

        status = self.__client.get_container_status(container)

        # 模块运行中则直接返回
        if status == DockerContainerStatus.RUNNING:
            return status

        if status == DockerContainerStatus.NOT_CREATED:
            if not self.__client.check_image(info["image"]):
                return DockerContainerStatus.NOT_LOADED

            if not auto_create:
                return status

            self.create_module_container(name, kind)

        self.__client.start_container(container)

        return self.__client.get_container_status(container)

    def stop_module_container(self, name: str, kind: str) -> DockerContainerStatus:
        """停止模块容器

        Args:
            name (str): 模块名称
            kind (str): 实现类型

        Returns:
            DockerContainerStatus: 模块容器类型
        """
        container = to_container_name(name, kind)

        self.__client.stop_container(container)

        return self.__client.get_container_status(container)

    def get_module_container_status(self, name: str, kind: str):
        docker_info = self.__info_dict[name][kind]

        if not self.__client.check_image(docker_info.image):
            return DockerContainerStatus.NOT_LOADED

        return self.__client.get_container_status(to_container_name(name, kind))

    def check_instance_has_docker(self, name: str, kind: str) -> bool:
        """校验实现实例是否存在 docker

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型

        Returns:
            bool: 结果
        """

        return self.__info_dict[to_container_name(name, kind)] is not None

    @property
    def info_list(self) -> List[Dict[str, Any]]:
        """获取 Docker 信息列表

        Returns:
            List[Dict[str, Any]]: _description_
        """
        result = []

        for container_name, instance in self.__info_dict.items():
            [name, kind] = container_name.split("_")
            result.append(
                {
                    "name": name,
                    "kind": kind,
                    "container_name": container_name,
                    "image": instance["image"],
                    "status": self.__client.get_container_status(container_name).value,
                }
            )

        return result


def __init_docker_client():
    try:
        return ModuleDockerClient()
    except Exception as e:
        print("docker connect error", repr(e))
        sys.exit()


DOCKER_CLIENT = __init_docker_client()

# {
#     "searcher": {
#         "es": {
#             "tag": "elasticsearch:8.13.4",
#             "envs": {
#                 "discovery.type": "single-node",
#                 "xpack.security.enabled": "false",
#             },
#             "ports": {"http": 9200, "tcp": 9300},
#         }
#     }
# }
