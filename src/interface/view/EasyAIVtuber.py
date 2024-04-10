import os
import subprocess
import requests


class EasyAIVtuber:
    def __init__(self, info: dict):
        self.port = info['port']
        self.url = f'http://localhost:{self.port}/alive'
        self.beat = info['beat']
        self.mouth_offset = info['mouth_offset']
        self.process = None
        self.character = info['character']
        self.output_size = info['output_size']
        self.simplify = info['simplify']
        self.output_webcam = info['output_webcam']
        self.model = info['model']
        self.sleep = info['sleep']
        self.port = info['port']
        pass

    def start(self):
        os.chdir("src\\interface\\view\\EasyAIVtuber")
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
        self.process = subprocess.run(command)

    def stop(self):
        self.process.kill()

    def speack(self, speech_path: str) -> dict:
        data = {}
        data["type"] = "speak"
        data["speech_path"] = speech_path
        return self.send_message(data)

    def swing(self, music_path: str, beat: int = None):
        if beat is None:
            beat = self.beat
        data = {}
        data["type"] = "rhythm"
        data["music_path"] = music_path
        data["beat"] = beat
        return self.send_message(data)

    def sing(self, music_path: str, voice_path: str, mouth_offset: float = None, beat: int = None):
        if mouth_offset is None:
            mouth_offset = self.mouth_offset
        if beat is None:
            beat = self.beat
        data = {}
        data["type"] = "sing"
        data["music_path"] = music_path
        data["voice_path"] = voice_path
        data["mouth_offset"] = mouth_offset
        data["beat"] = beat
        return self.send_message(data)

    def stop_move(self):
        data = {
            "type": "stop"
        }
        return self.send_message(data)

    def change_img(self, img_path: str):
        data = {}
        data["type"] = "change_img"
        data["img"] = img_path
        return self.send_message(data)

    def send_message(self, data: dict) -> dict:
        res = requests.post(self.url, json=data)
        return res.json()
