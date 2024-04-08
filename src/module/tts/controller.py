from enum import Enum

from local_tts import LocalTTS
from api_tts import ApiTTS


class TTS_TYPE(Enum):
    API = 1
    LOCAL = 2


class TTSController:
    def __init__(self):
        self.api_tts = ApiTTS()
        self.local_tts = LocalTTS()
        self.tts_type = TTS_TYPE.API

    def change(self, tts_type: TTS_TYPE, name: str):
        pass

    def generate_speech(self, text):
        if self.tts_type == TTS_TYPE.API:
            return self.api_tts.synthesize(text)
        elif self.tts_type == TTS_TYPE.LOCAL:
            return self.local_tts.synthesize(text)
