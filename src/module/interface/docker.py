from typing import Dict

import docker
import docker.errors
import docker.types

from .info import ModuleDockerInfo

HOST = "127.0.0.1"
PORT = 2375


def generate_url(host: str, port: int):
    return f"tcp://{host}:{port}"


class DockerClient:
    def __init__(self):
        self._client = docker.DockerClient(base_url=generate_url(HOST, PORT))

        print(self._client.images.list())

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

    def create_container(
        self,
        image_name: str,
        name: str,
        envs: dict | None = None,
        ports: Dict[str, int] | None = None,
        no_exists: bool = False,
    ):
        # 端口映射: https://www.jianshu.com/p/c1bfc14d5c02
        # 环境变量: https://stackoverflow.com/questions/67482434/set-environment-var-to-docker-container-created-in-python

        # 如果要求不存在，此时容器，则不会创建
        if no_exists and self.check_container(name):
            return False

        self._client.containers.create(
            image_name, name=name, environment=envs, ports=ports
        )

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

    def _get_container(self, name: str):
        return self._client.containers.get(name)


def __to_container_name(name: str, kind: str):
    return f"{name}_{kind}"


class ModuleDockerClient(DockerClient):
    def create_module_container(
        self,
        name: str,
        kind: str,
        docker_info: ModuleDockerInfo,
        no_exists: bool = False,
    ):

        name = __to_container_name(name, kind)

        # 对端口信息进行封装
        ports = {}
        for content in docker_info.ports.values():
            source = f"{content.in_port}/{content.protocol}"
            ports[source] = content.out_port

        super().create_container(
            docker_info.tag, name, docker_info.envs, ports, no_exists
        )

    def start_module_container(self, name: str, kind: str):
        super().start_container(__to_container_name(name, kind))

    def stop_module_container(self, name: str, kind: str):
        super().start_container(__to_container_name(name, kind))
