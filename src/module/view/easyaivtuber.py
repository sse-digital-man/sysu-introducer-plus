import subprocess
import requests
from typing import Dict
from module.view.interface import ViewInterface

def get_url(port: str) -> str:
    return f'http://localhost:{port}/alive'

class EasyaivtuberView(ViewInterface):
    def __init__(self):
        super().__init__()

        # 设置启动参数
        self.__startup_args = {}

        self.__url = get_url(7888)
        self.__beat = 1
        self.__mouth_offset = 0.

    def _load_config(self):
        # 该函数的父类函数是抽象函数
        # super()._load_config()
        info = self._read_config()

        def is_startup_arg(name: str) -> bool:
            # 排除非启动参数
            return not (name in ["beat", "mouth_offset"])
        
        # 1. 设置启动参数
        for key, value in info.items():
            if is_startup_arg(key):
                self.__startup_args[key] = value

        # 2. 设置生成参数
        self.__url = get_url(info["port"])
        self.__beat = info['beat']
        self.__mouth_offset = info['mouth_offset']

    def _run_command(self):
        command = [ "python", "main.py" ]
        for key, value in self.__startup_args.items():
            command.extend([f"--{key}", value])
        
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
            data["mouth_offset"] = self.__mouth_offset
            data["beat"] = self.__beat
        print(data)
        return self.send_message(data)

    def background_music(self, path: str, beat: int = None) -> Dict[str, str]:
        if beat is None:
            beat = self.beat
        data = {}
        data["type"] = "rhythm"
        data["music_path"] = path
        data["beat"] = self.__beat
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
        res = requests.post(self.__url, json=data)
        return res.json()
