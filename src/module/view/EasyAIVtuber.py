import requests
from typing import Dict, List
from module.view.interface import ViewInterface


class EasyAIVtuber(ViewInterface):
    def _load_config(self):
        super()._load_config()

    def speak(self, path: str, bgm_path: str = None, mouth_offset: float = None, beat: int = None) -> Dict[str, str]:
        data = []
        if bgm_path is None:
            data["type"] = "speak"
            data["speech_path"] = path
        else:
            if mouth_offset is None:
                mouth_offset = self.mouth_offset
            if beat is None:
                beat = self.beat
            data = {}
            data["type"] = "sing"
            data["music_path"] = bgm_path
            data["voice_path"] = path
            data["mouth_offset"] = mouth_offset
            data["beat"] = beat
        return self.send_message(data)

    def background_music(self, path: str, beat: int = None) -> Dict[str, str]:
        if beat is None:
            beat = self.beat
        data = {}
        data["type"] = "rhythm"
        data["music_path"] = path
        data["beat"] = beat
        return self.send_message(data)

    def stop_move(self) -> Dict[str, str]:
        data = {
            "type": "stop"
        }
        return self.send_message(data)

    def change_img(self, img_path: str):
        data = {}
        data["type"] = "change_img"
        data["img"] = img_path
        return self.send_message(data)

    def send_message(self, data: dict) -> Dict[str, str]:
        res = requests.post(self.url, json=data)
        return res.json()
