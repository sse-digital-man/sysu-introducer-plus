from abc import abstractmethod, ABCMeta
from typing import List, Dict, Any, Callable, Self
from threading import Thread

from utils.time import now, sub_time
from message import Message

from .info import ModuleStatus, ModuleName
from .log import HandleLog, LOGGER


class BasicModule(metaclass=ABCMeta):
    def __init__(self):
        """初始化函数，注意不要在此处编写过多地初始化操作

        Args:
            name (str): 模块名称
        """
        # 模块的基本信息
        super().__init__()

        # 依赖注入
        self.__name = None
        self.__kind = None
        self.__status = ModuleStatus.NotLoaded
        self.__sub_modules: Dict[str, Self | None]

        # 模块的配置信息由 Cell 进行注入
        self.__config: Dict[str, Any] = {}

        self.__has_injected = False

        # 线程相关
        self.__threads: List[Thread] = []

    @staticmethod
    def _handle_log(fn):
        def wrapper(self: Self, *args):
            # 如果不是在运行中调用，则
            if self.status is not ModuleStatus.Started:
                return fn(self, *args)

            start_time = now()

            # 处理结果
            result = fn(self, *args)

            # 记录处理日志
            LOGGER.log(HandleLog(self.name, self.kind, sub_time(start_time, now())))

            return result

        return wrapper

    # 该函数主要由模块管理器统一进行管理，统一进行更新
    @abstractmethod
    def load_config(self):
        # 需要每次更新配置文件以保证最新
        pass

    def check(self):
        """验证模块是否能够正常运行，成功无需处理，失败则会抛出异常。

        Raises:
            BaseExceptions: 产生错误
        """

    def _read_config(self) -> Dict:
        return self.__config

    # 开辟一个线程用于处理
    def _make_thread(self, target: Callable):
        thread = Thread(target=target)
        self.__threads.append(thread)
        thread.start()

    def wait_threads(self):
        for thread in self.__threads:
            thread.join()

    # ----- Hook -----

    def before_starting_submodules(self):
        """启动子模块之前的钩子函数（在模块自定义启动逻辑之前）"""

    def handle_starting(self):
        """模块自定义启动逻辑（在启动子模块之后）"""

    def handle_stopping(self):
        """模块自定义停止逻辑（在停止子模块之前）"""

    def after_stopping_submodules(self):
        """停止子模块之后的钩子函数（在模块自定义停止逻辑之后）"""

    # ----- Getter ----- #
    @property
    def name(self) -> str:
        return self.__name

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def status(self) -> ModuleStatus:
        return self.__status

    @property
    def is_running(self) -> bool:
        return self.status is ModuleStatus.Started

    @property
    def _is_ready(self) -> bool:
        """判断当前模块是否满足线程的运行条件, 主要模块内部可控制线程运行

        Returns:
            bool: 结果
        """

        return self.status in [ModuleStatus.Started, ModuleStatus.Starting]

    # 获取子模块的对象
    def _sub_module(self, name: str | ModuleName) -> Self:
        if isinstance(name, ModuleName):
            name = name.value

        try:
            # Notice: 不能直接比较 None, 因为未加载的模块返回为空
            return self.__sub_modules[name]
        except KeyError:
            raise FileNotFoundError(f"{name} is not in {self.name}")

    #  ----- Setter -----

    # ----- 管理器依赖注入 -----

    def inject(
        self, name: str, kind: str, sub_modules: Dict[str, Self], config: Dict[str, Any]
    ):
        """管理器初次注入信息

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型
            sub_modules (Dict[str, Self]): 子模块对象指针
        """

        if self.__has_injected:
            raise RuntimeError("object of module has been injected")

        self.__name = name
        self.__kind = kind
        self.__sub_modules = sub_modules
        self.__config = config

        self.__has_injected = True

    def update_status(self, status: ModuleStatus):
        self.__status = status

    def update_submodule(self, name: str, sub_module: Self):
        """更新模块的子模块指针，由于子模块可能为空，因此需要传入名称

        Args:
            name (str): 模块名称
            sub_module (Self): 子模块指针
        """
        self.__sub_modules[name] = sub_module


class BooterInterface(BasicModule, metaclass=ABCMeta):
    def send(self, _message: Message): ...
