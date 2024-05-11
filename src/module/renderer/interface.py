from abc import ABCMeta, abstractmethod
from typing import List, Dict

from module.interface import BasicModule


class RendererInterface(BasicModule, metaclass=ABCMeta):
    Kind = "renderer"

    def __init__(self):
        super().__init__(self.Kind)

    @abstractmethod
    def speak(self, path: str) -> Dict[str, str]:
        """数字人视图说话，并播放 path 路径下的音频文件

        Args:
            path (str): 音频文件路径

        Returns:
            Dict[str, str]: 返回结果
        """
        ...

    @abstractmethod
    def background_music(self, path: str) -> Dict[str, str]:
        """数字人背景音乐，播放 path 路径下的音乐

        Args:
            path (str): 音频文件路径

        Returns:
            Dict[str, str]: 返回结果
        """
        ...

    @abstractmethod
    def stop_move(self) -> Dict[str, str]:
        """停止数字人任何动作
        """
        ...
