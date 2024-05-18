from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Tuple
from module.interface import BasicModule
import os
import time
from typing import Tuple


class SpeakerInterface(BasicModule, metaclass=ABCMeta):
    def _generate_filename(self, suffix: str = "wav") -> str:
        return (
            datetime.now().strftime(f"{self.__class__.__name__}-%Y%m%d%H%M%S")
            + f".{suffix}"
        )
    
    def check(self) -> Tuple[bool, Exception | None]:
        total_time = 60
        iter_time = 10
        for _ in range(total_time // iter_time):
            try:
                output_path = self.speak("你好，我是中大校史介绍官中小大，很高兴能为您介绍中大校史。")
                if os.path.exists(output_path):
                    return True, None
                else:
                    return False, Exception()
            except Exception as e:
                print(e)
                time.sleep(iter_time)

        return False, TimeoutError()

    @abstractmethod
    def speak(self, text) -> str:
        pass
