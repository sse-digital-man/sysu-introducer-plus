from typing import Dict, Any, Self

from utils import error

from .. import BasicModule
from ..info import ModuleInfo, ModuleStatus
from ..log import LOGGER, StatusLog
from ..config import ModuleConfig

from .utils import dynamic_import_module, NULL


class ModuleManageCell:
    def __init__(self, info: ModuleInfo, kind: str | None = None):
        self._info = info
        self._status: ModuleStatus = ModuleStatus.NotLoaded
        self._kind: str = info.default if kind is None else kind

        # 模块对象指针
        self._module: BasicModule = None

        # 配置文件
        self._config: ModuleConfig = None

        # 记录管理单元的父子关系
        self._sup: ModuleManageCell | None = None
        self._sub: Dict[str, ModuleManageCell] = {}

        self._load_module()

    def _load_module(self):
        # 如果需要加载的模块类型为空，则表示仍未加载
        if self._kind == NULL:
            self._module = None
            self.update_status(ModuleStatus.NotLoaded)
        else:
            module_object = dynamic_import_module(self._info, self._kind)
            self._module = module_object()
            self.update_status(ModuleStatus.Stopped)

    # Notice: 将 inject 与 load_module 分离
    def inject(self):
        if self._module is None:
            return

        submodules = {name: sub_cell.module for name, sub_cell in self._sub.items()}
        config = None if self._config is None else self._config.instance(self._kind)

        self._module.inject(self._info.name, self._kind, submodules, config)

    def start(self, with_sub: bool = True, with_sup: bool = False):
        """启动模块。
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

        # 0. 如果当前模块状态不是在停止状态 则不能停止
        cur_status = self._status
        if cur_status != ModuleStatus.Stopped:
            return False, cur_status

        # 1. 首先启动启动子模块
        module = self._module
        module.before_starting_submodules()

        self.update_status(ModuleStatus.Starting)

        if with_sub:
            for sub_cell in self._sub.values():
                if sub_cell.is_null:
                    continue

                sub_cell.start(with_sub=True, with_sup=False)

        # 2. 更新配置信息
        try:
            module.load_config()
        except KeyError:
            raise error.ModuleRuntimeError(
                f"configuration about module '{module.name}' is missing"
            )

        # 3. 模块的自定义启动逻辑
        module.handle_starting()

        # 4. 模块自检
        try:
            module.check()
        except BaseException as e:
            raise error.ModuleCheckError(self.name, e)

        # 5. 钩子函数
        self.update_status(ModuleStatus.Started)

        if with_sup and self._sup is not None:
            self._sup.start(with_sub=False, with_sup=True)

    def stop(self):
        """停止模块

        Args:
            name (str): 模块名称

        Returns:
            bool: 是否运行成功，当前的状态（运行成功为None）
        """

        # 运行成功之后可以停止, 发生异常需要级联停止
        if not (
            self._status == ModuleStatus.Started or ModuleStatus.is_error(self._status)
        ):
            return

        module = self._module

        # 1. 先设置标志位
        module.handle_stopping()
        self.update_status(ModuleStatus.Stopping)

        # 2. 关闭内部的线程处理
        module.wait_threads()

        # 3. 关闭子线程
        for sub_cell in self._sub.values():
            if sub_cell.is_null:
                continue
            sub_cell.stop()

        module.after_stopping_submodules()

        self.update_status(ModuleStatus.Stopped)

    def change_module_kind(self, kind: str):
        """切换模块的实现类型，并返回是否切换成功

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型

        Raises:
            FileNotFoundError: 模块不存在
            ValueError: 模块实现类型不支持

        Returns:
            Tuple[bool, ModuleStatus]: 是否切换成功、当前状态（切换成功为空）
        """

        # 判断模块状态是否可切换
        if not ModuleStatus.can_change(self.status):
            return

        # 验证类型是否满足条件
        self._check_kind_exist(kind)

        # 加载模块并进行依赖注入
        self._kind = kind
        self._load_module()
        self.inject()

        # 2. 重新设置父模块中的指针
        if self._sup is not None:
            # 更新父模块的子模块
            self._sup.update_submodule(self.name, self._module)

    def modify_instance_config(self, kind: str, content: Dict[str, Any]):
        self._check_kind_exist(kind)
        # 由于 Module 内的对象指向同一块配置信息 Dic，因此不需要修改对象中的配置文件
        self.config.update_instance(kind, content)

    def _check_kind_exist(self, kind: str):
        if kind not in self._info.kinds:
            raise error.ModuleLoadError(
                f"the kind '{kind}' is not supported in {self.name}"
            )

    @property
    def name(self) -> str:
        return self._info.name

    @property
    def info(self) -> ModuleInfo:
        return self._info

    @property
    def config(self) -> ModuleConfig:
        return self._config

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def status(self) -> ModuleStatus:
        return self._status

    @property
    def module(self) -> BasicModule:
        return self._module

    @property
    def is_null(self) -> bool:
        return self._module is None

    def update_status(self, status: ModuleStatus):
        self._status = status
        if self._module is not None:
            self._module.update_status(status)

        LOGGER.log(StatusLog(self.name, status))

    def update_submodule(self, name: str, module: BasicModule):
        self._module.update_submodule(name, module)

    def set_sub(self, name: str, sub_cell: Self):
        self._sub[name] = sub_cell

    def set_sup(self, sup_cell: Self):
        self._sup = sup_cell

    def set_config(self, config: ModuleConfig):
        self._config = config
