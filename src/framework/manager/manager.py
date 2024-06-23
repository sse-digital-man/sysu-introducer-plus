from typing import Dict, List, Any

from utils import error

from message import Message
from .. import RootInterface
from ..info import ModuleStatus, to_instance_label

from .cell import ModuleManageCell
from .load import ModuleLoader


class ModuleManager:
    def __init__(self):
        self.__loader = ModuleLoader()

        self.__root_cell: ModuleManageCell = None
        self.__cell_pool: Dict[str, ModuleManageCell] = []

    def load(self):
        self.__loader.load()

        self.__root_cell = self.__loader.root_cell
        self.__cell_pool = self.__loader.cell_pool

    # ----- 模块控制 ----- #

    # 启动模块单元
    def start(self, name: str, with_sub: bool = True, with_sup: bool = False):
        """启动模块
        注意递归启动有方向性，递归父模块时只会递归启动父模块，子模块同理

        Args:
            name (str): 模块名称
            with_sub (bool, optional): 是否递归启动父模块. Defaults to True.
            with_sup (bool, optional): 是否递归启动父模块. Defaults to False.

        Raises:
            FileNotFoundError: _description_
            e: _description_

        Returns:
            Tuple[bool, ModuleStatus]: 是否运行成功，当前的状态（运行成功为None）
        """

        cell = self._cell(name, force=True)

        try:
            cell.start(with_sub, with_sup)
        except error.ModuleError as e:
            # 如果模块启动曹组
            cell.update_status(cell, ModuleStatus.StartError)
            cell.stop()
            raise e

    def stop(self, name: str):
        cell = self._cell(name, force=True)
        cell.stop()

    def send(self, msg: Message):
        if self.__root_cell is None:
            return

        # 只能通过 booter 进行交互
        booter: RootInterface = self.__root_cell.module
        booter.send(msg)

    def change_module_kind(self, name: str, kind: str):
        self._cell(name, force=True).change_module_kind(kind)

    def modify_instance_config(self, name: str, kind: str, config: Dict[str, Any]):
        """修改指定模块实现实例的配置

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型
            config (Dict[str, Any]): 配置文件内容

        Raises:
            error.ModuleRuntimeError: _description_
        """

        cell = self._cell(name, force=True)
        # 通过管理单元更新
        cell.modify_instance_config(kind, config)
        # 持久化到本地文件
        self.__loader.save_instance_config(name, kind, config)

    # ----- Getter ----- #
    def _cell(self, name: str, force: bool = True) -> ModuleManageCell:
        cell = self.__module_cells.get(name)

        if cell is None and force:
            raise error.ModuleRuntimeError(f"module '{name}' not found")

        return cell

    def check_module_exist(self, name: str) -> bool:
        return name in self.__module_cells.values()

    def is_controllable(self, name: str) -> bool:
        return name == self.__root_cell.name or name in self.__root_cell.info.sub

    @property
    def module_info_list(self) -> List[dict]:
        """列表组成 name, alias, kind, status

        Returns:
            List[Dict]: 信息的列表
        """

        result = []
        for _, cell in self.__cell_pool.items():

            result.append(
                {
                    "name": cell.name,
                    "kind": cell.kind,
                    "alias": cell.info.alias,
                    "submodules": [
                        to_instance_label(sub_cell.name, sub_cell.kind)
                        for sub_cell in cell.sub_cells.values()
                    ],
                    "status": cell.status,
                }
            )

        # 可以不排序，默认是嵌套关系的顺序
        # result = sorted(result, key=lambda item: item["name"])

        return result

    @property
    def module_info_tree(self) -> Dict:
        """返回以根模块信息字典对应的节点

        Returns:
            Dict: 根模块字典
        """
        result_map = {}

        def __translate(cell: ModuleManageCell):
            instance_label = to_instance_label(cell.name, cell.kind)

            # 如果 result 重复就不需要重复创建
            if instance_label not in result_map:
                result = cell.cell_info

                if len(cell.sub_cells) > 0:
                    result["submodules"] = [
                        __translate(sub_cell) for sub_cell in cell.sub_cells.values()
                    ]

                result_map[instance_label] = result

            return result_map[instance_label]

        return __translate(self.__root_cell)

    @property
    def user_config_list(self):
        """返回用户配置列表

        Returns:
            Dict[str, dict]: _description_
        """
        return {
            name: cell.config.user_config
            for name, cell in self.__module_cells.items()
            if len(cell.config.user_config) > 0
        }
