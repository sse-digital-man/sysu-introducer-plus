from typing import List, Dict, Any
from pathlib import Path

from docker.types import DeviceRequest

from framework.info import to_instance_label
from utils.file import load_yaml


def _parse_gpu(gpus: str | None) -> List[DeviceRequest]:
    if gpus == "all":
        return [DeviceRequest(count=-1)]

    return None


# def _load_single_docker_info(instance: dict):
#     # 处理端口的语法糖
#     format_ports = {}
#     for field, content in instance["ports"].items():
#         if isinstance(content, int):
#             port = ModuleDockerInfo.Port(content, content)
#         elif isinstance(content, dict):
#             in_port = content["in"]
#             port = ModuleDockerInfo.Port(
#                 in_port,
#                 content.get("out", in_port),
#                 content.get("protocol", "tcp"),
#             )
#         else:
#             raise ValueError("docker config info error")

#         format_ports[field] = port

#     return ModuleDockerInfo(
#         instance["image"],
#         instance.get("envs", {}),
#         format_ports,
#         _parse_gpu(instance.get(GPUS)),
#         instance.get("shm_size"),
#     )

GPUS = "gpus"
DEVICE_REQUESTS = "device_requests"
VOLUMES = "volumes"


# 对单条 Docker 配置进行预处理
def _process_single_docker_config(instance: dict):
    if GPUS in instance:
        gpus = instance[GPUS]
        if gpus == "all":
            instance[DEVICE_REQUESTS] = [DeviceRequest(count=-1)]

        instance.pop(GPUS)

    if VOLUMES in instance:
        volumes: List[str] = instance[VOLUMES]
        for i, volume in enumerate(volumes):
            [src, dst] = volume.split(":")

            src_path = Path(src)
            if src_path.is_absolute():
                continue

            src = str(src_path.absolute())
            volumes[i] = f"{src}:{dst}"

    return instance


def load_docker_config(
    path: str,
) -> Dict[str, dict]:
    raw_docker: Dict[str, Dict[str, Any]] = load_yaml(path)

    docker_config = {}
    # 读取关于 Docker 相关的配置信息
    for name, module in raw_docker.items():
        # 如果模块对应的 Docker 信息为空，则直接跳过
        for kind, instance in module.items():
            docker_config[to_instance_label(name, kind)] = (
                _process_single_docker_config(instance)
            )

    return docker_config
