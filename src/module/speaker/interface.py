from module.interface import BasicModule
from abc import ABCMeta, abstractmethod
from datetime import datetime

class SpeakerInterface(BasicModule, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def _load_config(self):
        pass

    def _generate_filename(self, suffix: str = 'wav') -> str:
        return datetime.now().strftime(f"{self.__class__.__name__}-%Y%m%d%H%M%S") + f'.{suffix}'

    @abstractmethod
    def speak(self, text) -> str:
        pass

