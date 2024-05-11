import subprocess
import requests
from typing import Dict
from module.view.interface import ViewInterface


class EasyaivtuberView(ViewInterface):
    def __init__(self):
        super().__init__()
        info = self._read_config()
        self.port = info['port']
        self.url = f'http://localhost:{self.port}/alive'
        self.beat = info['beat']
        self.mouth_offset = info['mouth_offset']

    def _load_config(self):
        super()._load_config()
        info = self._read_config()
        self.character = info['character']
        self.output_size = info['output_size']
        self.simplify = info['simplify']
        self.output_webcam = info['output_webcam']
        self.model = info['model']
        self.sleep = info['sleep']

    def _run_command(self):
        command = [
            "python", "main.py",
            "--character", str(self.character),
            "--output_size", str(self.output_size),
            "--simplify", str(self.simplify),
            "--output_webcam", str(self.output_webcam),
            "--model", str(self.model),
            "--anime4k",
            "--sleep", str(self.sleep),
            "--port", str(self.port)
        ]
        # 通过cwd参数指定工作目录
        subprocess.run(
            command, cwd='src/module/view/EasyAIVtuber/')

    def _before_started(self):
        super()._before_started()
        self._make_thread(self._run_command)

    def speak(self, path: str, bgm_path: str = None, mouth_offset: float = None, beat: int = None) -> Dict[str, str]:
        data = {}
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
        print(data)
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
