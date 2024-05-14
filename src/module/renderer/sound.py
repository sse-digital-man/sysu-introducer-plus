from typing import Dict
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

from .interface import RendererInterface


# https://blog.csdn.net/pengranxindong/article/details/90606279


class SoundRenderer(RendererInterface):
    def load_config(self):
        pass

    def speak(self, path: str):
        sound = AudioSegment.from_file(path, format=Path(path).suffix)
        play(sound)

    def background_music(self, path: str) -> Dict[str, str]:
        pass

    def stop_move(self) -> Dict[str, str]:
        pass
