from typing import Dict, List, Any

from utils import error

from message import Message
from .. import BooterInterface
from ..info import ModuleStatus

from .cell import ModuleManageCell
from .load import ModuleLoader


class ModuleManager:
    def __init__(self):
        self.__loader = ModuleLoader()

        self.__module_cells: Dict[str, ModuleManageCell] = {}
        # Notice: 模块依赖树的根节点必须是一个 Booter
        self.__booter_cell: ModuleManageCell = None

    def load(self):
        self.__loader.load()

        self.__module_cells = self.__loader.module_cells
        self.__booter_cell = self.__loader.booter_cell

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
        if self.__booter_cell is None:
            return

        # 只能通过 booter 进行交互
        booter: BooterInterface = self.__booter_cell.module
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
        return name == self.__booter_cell.name or name in self.__booter_cell.info.sub

    @property
    def module_list(self) -> List[Dict]:
        """列表组成 name, alias, kind, status

        Returns:
            List[Dict]: 信息的列表
        """

        info_list = []

        for cell in self.__module_cells.values():
            info_dict = cell.info.to_dict()

            # 添加状态信息
            info_dict["status"] = cell.status
            info_dict["kind"] = cell.kind
            info_list.append(info_dict)

        return info_list

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
