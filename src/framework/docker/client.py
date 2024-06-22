import sys
from typing import List, Dict, Any
from time import sleep

import docker
import docker.errors
import docker.types

from .info import ModuleDockerInfo, DockerContainerStatus
from .parser import _parser_docker_info

# Macos Docker 启动配置
# socat TCP-LISTEN:2375,reuseaddr,fork UNIX-CONNECT:/var/run/docker.sock &

HOST = "127.0.0.1"
PORT = 2375

RUNNING = "running"

DOCKER_PATH = "docker.yaml"


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

        # TODO: 优化自旋锁逻辑
        waiting_time = 15
        cur_time = 0
        while cur_time < waiting_time:
            sleep(5)
            cur_time += 5

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


def _to_container_name(name: str, kind: str):
    return f"{name}_{kind}"


class ModuleDockerClient(DockerClient):
    def __init__(self):
        self.__docker_info_list = _parser_docker_info(DOCKER_PATH)

        super().__init__()

    def create_module_container(
        self,
        name: str,
        kind: str,
        docker_info: ModuleDockerInfo,
        no_exists: bool = False,
    ):

        name = _to_container_name(name, kind)

        # 对端口信息进行封装
        ports = {}
        for content in docker_info.ports.values():
            source = f"{content.in_port}/{content.protocol}"
            ports[source] = content.out_port

        super().create_container(
            docker_info.image, name, docker_info.envs, ports, no_exists
        )

    def start_module_container(self, name: str, kind: str):
        container = _to_container_name(name, kind)
        # 模块运行中则直接返回
        if self.get_container_status(container) == DockerContainerStatus.RUNNING:
            return DockerContainerStatus.RUNNING

        super().start_container(container)

        return self.get_container_status(container)

    def stop_module_container(self, name: str, kind: str):
        container = _to_container_name(name, kind)

        super().stop_container(container)

        return self.get_container_status(container)

    def get_module_container_status(
        self, name: str, kind: str, docker_info: ModuleDockerInfo
    ):
        if not self.check_image(docker_info.tag):
            return DockerContainerStatus.NOT_LOADED

        return self.get_container_status(_to_container_name(name, kind))

    def check_instance_has_docker(self, name: str, kind: str) -> bool:
        """校验实现实例是否存在 docker

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型

        Returns:
            bool: 结果
        """

        info_dict = self.__docker_info_list

        if name not in info_dict or kind not in info_dict[name]:
            return False

        return info_dict[name][kind] is not None

    @property
    def docker_info_list(self) -> List[Dict[str, Any]]:
        """获取 Docker 信息列表

        Returns:
            List[Dict[str, Any]]: _description_
        """
        result = []

        for name, module in self.__docker_info_list.items():
            for kind, instance in module.items():
                container = _to_container_name(name, kind)

                result.append(
                    {
                        "moduleName": name,
                        "moduleKind": kind,
                        "name": container,
                        "image": instance.image,
                        "status": self.get_container_status(container).value,
                    }
                )

        return result


def __init_docker_client():
    try:
        return ModuleDockerClient()
    except Exception as e:
        raise e
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
