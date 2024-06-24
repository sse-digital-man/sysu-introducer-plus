from enum import Enum


class DockerContainerStatus(Enum):
    NOT_LOADED = 0
    NOT_CREATED = 1
    RUNNING = 2
    EXITED = 3


dockerStatusMap = {
    DockerContainerStatus.NOT_LOADED: "未加载",
    DockerContainerStatus.NOT_CREATED: "未创建",
    DockerContainerStatus.RUNNING: "运行中",
    DockerContainerStatus.EXITED: "停止中",
}
