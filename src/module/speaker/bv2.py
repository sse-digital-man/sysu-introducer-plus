import os
import subprocess
import requests

from .interface import SpeakerInterface


class Bv2Speaker(SpeakerInterface):
    def __init__(self):
        super().__init__()
        self.__host = "127.0.0.1"
        self.__port = 5000
        self.__url = f"http://{self.__host}:{self.__port}/voice"
        self.__output_dir = "./data/sound"

    def load_config(self):
        pass

    def speak(self, text) -> str:
        # 此处应在start后调用
        # 拼接请求构成GET请求
        query = self.__url
        print(query)

        params = {
            "model_id": 0,
            "speaker_name": "babala",
            "sdp_ratio": 0.2,
            "noise": 0.2,
            "noisew": 0.9,
            "length": 1,
            "language": "ZH",
            "auto_translate": "false",
            "auto_split": "false",
            "emotion": "",
            "style_weight": 0.7,
        }

        files = {
            "text": (None, text),
        }

        response = requests.post(query, params=params, files=files)

        if response.status_code == 200:
            # 获取音频流内容
            audio_data = response.content
            print(response.headers)

            # 将音频流保存到文件中
            file_name = self._generate_filename()
            output_path = os.path.join(self.__output_dir, file_name)
            with open(output_path, "wb") as f:
                f.write(audio_data)

            return output_path
        else:
            raise RuntimeError()

    def handle_starting(self):
        root_path = "src/module/speaker/BV2/"
        program_path = "hiyoriUI.py"
        interpreter_path = "C:/Users/Student/anaconda3/envs/BV2/python.exe"

        command = [
            interpreter_path,
            program_path,
        ]

        subprocess.Popen(command, cwd=root_path, shell=True, env=os.environ)
