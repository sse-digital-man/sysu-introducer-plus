from typing import Dict, Any

from utils.file import load_yaml
from .info import ModuleDockerInfo


def _parser_docker_info(
    path: str,
) -> Dict[str, Dict[str, ModuleDockerInfo]]:
    raw_docker: Dict[str, Dict[str, Any]] = load_yaml(path)

    docker_config = {}
    # 读取关于 Docker 相关的配置信息
    for name, module in raw_docker.items():
        # 如果模块对应的 Docker 信息为空，则直接跳过
        docker_config[name] = {}
        for kind, instance in module.items():

            # 处理端口的语法糖
            format_ports = {}
            for field, content in instance["ports"].items():
                if isinstance(content, int):
                    port = ModuleDockerInfo.Port(content, content)
                elif isinstance(content, dict):
                    in_port = content["in"]
                    port = ModuleDockerInfo.Port(
                        in_port,
                        content.get("out", in_port),
                        content.get("protocol", "tcp"),
                    )
                else:
                    raise ValueError("docker config info error")

                format_ports[field] = port
            docker_config[name][kind] = ModuleDockerInfo(
                instance["image"], instance["envs"], format_ports
            )

    return docker_config
