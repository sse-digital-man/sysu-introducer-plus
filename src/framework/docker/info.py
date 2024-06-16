from typing import Dict
from enum import Enum


class ModuleDockerInfo:
    class Port:
        def __init__(self, in_port: int, out_port: int, protocol: str = "tcp"):
            self.in_port = in_port
            self.out_port = out_port
            self.protocol = protocol

    def __init__(self, image: str, envs: Dict[str, str], ports: Dict[str, Port]):
        self.image = image
        self.envs = envs
        self.ports = ports

    def out_port(self, field: str):
        return self.ports[field].out_port


class DockerContainerStatus(Enum):
    NOT_LOADED = 0
    NOT_CREATED = 1
    RUNNING = 2
    EXITED = 3
