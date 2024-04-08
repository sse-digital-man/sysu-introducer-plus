from abc import ABCMeta, abstractmethod
from datetime import datetime


class TTSInterface(metaclass=ABCMeta):
    """TTS interface."""
    @staticmethod
    def generate_filename(prefix: str, suffix: str) -> str:
        """generate filename base on prefix-current time-suffix."""
        return f"{prefix}-{datetime.now().strftime('%Y%m%d%H%M%S')}{suffix}"

    @abstractmethod
    def synthesize(self, input_data: str) -> str:
        """synthesize output based on the input data."""
        pass

    @abstractmethod
    def change(self, name: str):
        """Change the api or model"""
        pass
