from abc import ABCMeta, abstractmethod
from datetime import datetime
from module.interface import BasicModule


class SpeakerInterface(BasicModule, metaclass=ABCMeta):
    def _generate_filename(self, suffix: str = "wav") -> str:
        return (
            datetime.now().strftime(f"{self.__class__.__name__}-%Y%m%d%H%M%S")
            + f".{suffix}"
        )

    @abstractmethod
    def speak(self, text) -> str:
        pass
