from typing import Dict, List, Any

from utils import error

from message import Message
from .. import RootInterface
from ..info import to_instance_label

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

    def _translate_full_name(self, full_name: str) -> List[ModuleManageCell]:
        """将 全模块名 解析校验，返回 cell 的列表
        1. "root.module1.module2": 以根模块打头
        2. ".module1.module2": 省略根模块名
        3. "module1.module2": 省略分隔符

        Args:
            full_name (str): 全模块名

        Returns:
             List[ModuleManageCell]: 分片结果
        """
        name_list = full_name.split(".")

        if len(name_list) == 0:
            raise error.ModuleRuntimeError("the full_name is empty")

        root_name = self.__root_cell.name

        if name_list[0] in [None, root_name]:
            name_list.pop(0)

        cur_cell = self.__root_cell
        cell_list = [cur_cell]
        while len(name_list) > 0:
            sub_name = name_list.pop(0)

            cell = cur_cell.sub_cells.get(sub_name)

            if cell is None:
                raise error.ModuleRuntimeError(
                    f"full_name is error, module '{sub_name}'w is not found"
                )

            cur_cell = cell
            cell_list.append(cell)

        return cell_list

    # 启动模块单元
    def start(self, full_name: str):
        """根据 全模块名 启动模块，其会启动包含链路的所有模块，
        以及最后模块的所有子模块。
        注意，在启动所在链路上的模块时，只会启动模块本身。

        Args:
            full_name (str): 全模块名
        """

        # 按照自底向上的启动顺序
        cell_list = self._translate_full_name(full_name)

        bottom_cell = cell_list.pop()
        bottom_cell.start(with_sub=True)

        cell_list.reverse()
        for cell in cell_list:
            try:
                cell.start(with_sub=False)
            except error.ModuleError as e:
                cell.stop()
                raise e

    def stop(self, full_name: str):
        cell_list = self._translate_full_name(full_name)
        cell_list[-1].stop()

    def send(self, msg: Message):
        if self.__root_cell is None:
            return

        # 只能通过 booter 进行交互
        booter: RootInterface = self.__root_cell.module
        booter.send(msg)

    def check_exist(self, full_name: str) -> bool:
        try:
            self._translate_full_name(full_name)
            return True
        except error.ModuleRuntimeError:
            return False

    def change_module_kind(self, name: str, kind: str):
        # self._cell(name, force=True).change_module_kind(kind)
        ...

    def modify_instance_config(self, name: str, kind: str, config: Dict[str, Any]):
        """修改指定模块实现实例的配置

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型
            config (Dict[str, Any]): 配置文件内容

        Raises:
            error.ModuleRuntimeError: _description_
        """

        # cell = self._cell(name, force=True)
        # # 通过管理单元更新
        # cell.modify_instance_config(kind, config)
        # # 持久化到本地文件
        # self.__loader.save_instance_config(name, kind, config)
        ...

    def is_controllable(self, name: str) -> bool:
        return name == self.__root_cell.name or name in self.__root_cell.info.sub

    @property
    def instance_list(self) -> List[dict]:
        """列表组成 name, alias, kind, status

        Returns:
            List[Dict]: 信息的列表
        """

        result = []
        for _, cell in self.__cell_pool.items():
            info = {
                "name": cell.name,
                "kind": cell.kind,
                "alias": cell.info.alias,
                "status": cell.status,
            }

            if len(cell.sub_cells) != 0:
                info["modules"] = [
                    to_instance_label(sub_cell.name, sub_cell.kind)
                    for sub_cell in cell.sub_cells.values()
                ]

            result.append(info)

        # 可以不排序，默认是嵌套关系的顺序
        # result = sorted(result, key=lambda item: item["name"])

        return result

    @property
    def instance_tree(self) -> Dict:
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
                    result["modules"] = [
                        __translate(sub_cell) for sub_cell in cell.sub_cells.values()
                    ]

                result_map[instance_label] = result

            return result_map[instance_label]

        return __translate(self.__root_cell)

    # @property
    # def user_config_list(self):
    #     """返回用户配置列表

    #     Returns:
    #         Dict[str, dict]: _description_
    #     """
    #     return {
    #         name: cell.config.user_config
    #         for name, cell in self.__module_cells.items()
    #         if len(cell.config.user_config) > 0
    #     }
