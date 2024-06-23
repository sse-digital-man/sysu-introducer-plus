from typing import Dict, Any
from utils.file import load_json

ConfigType = Dict[str, Dict[str, Dict[str, Any]]]

NUMBER = "number"
STRING = "string"
BOOLEAN = "boolean"

CONFIG_ITEM_TYPE_MAP = {"number": int, "string": str, "boolean": bool}


def check_config_item_kind(value: Any, item_type: str):
    if item_type not in CONFIG_ITEM_TYPE_MAP:
        raise RuntimeError("unknown type")

    if not isinstance(value, CONFIG_ITEM_TYPE_MAP.get(item_type)):
        raise RuntimeError("config item type error")


# 配置项的格式
class ConfigItemFormat:
    def __init__(self, field: str, label: str, item_type: str):
        self._field = field
        self._label = label
        self._type = item_type

    def to_dict(self):
        return {"label": self._label, "type": self._type}

    @property
    def item_type(self) -> str:
        return self._type


# 模块的配置内容
class ModuleConfig:
    def __init__(
        self,
        data: Dict[str, Dict[str, Any]],
        config_format: Dict[str, Dict[str, ConfigItemFormat]],
    ):
        # 由于对于模块配置本身而言，其并需要关注 System 和 User 的区别
        # 所以只需要存储 System 即可，且由 user_format 进行约束
        self._data = data
        self._format = config_format

    def instance(self, kind: str) -> Dict[str, Any] | None:
        """获取实现实例对应的配置信息

        Args:
            kind (str): 实现类型

        Returns:
            Dict[str, Any] | None: 配置内容
        """
        return self._data.get(kind, None)

    def update_instance(self, kind: str, content: Dict[str, Any]):
        """更新实现实例的的配置信息

        Args:
            kind (str): 实现类型
            content (Dict[str, Any]): 配置内容
        """
        user_format = self._format.get(kind, None)
        if user_format is None:
            raise KeyError(f"instance '{kind}' not found")

        for field, value in content.items():
            if field not in user_format.keys():
                raise KeyError(f"config item '{field}' not found in instant '{kind}'")

            check_config_item_kind(value, user_format[field].item_type)

        for field, value in content.items():
            self._data[kind][field] = value

    @property
    def user_config(self) -> Dict[str, Dict[str, Any]]:
        """配置格式和配置数据合并在一起

        Returns:
            Dict[str, Dict[str, Any]]: 组合结果
        """
        user_config = {}

        for kind, instance in self._format.items():
            user_config[kind] = {}
            for field, content in instance.items():
                config_item = content.to_dict()
                config_item["value"] = self._data[kind][field]

                user_config[kind][field] = config_item

        return user_config


def load_config(system_path: str, user_path: str, user_format_path):
    # system 提供所有配置信息的初始值，user 提供可供用户配置的用户
    system_data: ConfigType = load_json(system_path)
    raw_user_data: ConfigType = load_json(user_path)
    # 原始的配置文件，此后需要转换为 ConfigItemFormat 对象
    raw_user_format: ConfigType = load_json(user_format_path)

    user_format: Dict[str, Dict[str, Dict[str, ConfigItemFormat]]] = {}
    for name, module in raw_user_format.items():
        user_format[name] = {}
        for kind, instant in module.items():
            user_format[name][kind] = {}
            for field, content in instant.items():
                # 1. 验证 UserFormat 中的关键信息
                if isinstance(content, str):
                    # 语法糖，转换成规范格式
                    label = content
                    item_type = STRING
                else:
                    label = content["label"]
                    item_type = content["type"]

                # 2. 创建对应的对象
                user_format[name][kind][field] = ConfigItemFormat(
                    field, label, item_type
                )

                # 3. 验证 UserFormat 要求的属性，User 和 System 存在且类型相同
                try:
                    user_value = raw_user_data[name][kind][field]
                    check_config_item_kind(user_value, item_type)
                except KeyError:
                    # User 可以不存在，但 System 一定要存在
                    pass

                try:
                    system_value = system_data[name][kind][field]
                    check_config_item_kind(system_value, item_type)
                except KeyError:
                    raise RuntimeError(f"{name} {kind} {field}")

    for name, module in raw_user_data.items():
        for kind, instant in module.items():
            for field, content in instant.items():
                # 将 User 配置覆盖到 System 中
                try:
                    system_data[name][kind][field] = content
                except KeyError:
                    #  User 出现 System中不存在的配置信息
                    raise RuntimeError(
                        "user config item can't be found in system config"
                    )

    return system_data, raw_user_data, user_format
