import os
import time
import subprocess
import requests

from .interface import SpeakerInterface


class GsvSpeaker(SpeakerInterface):
    def __init__(self):
        super().__init__()
        self.__host = "127.0.0.1"
        self.__port = 9880
        self.__url = f"http://{self.__host}:{self.__port}/"
        self.__output_dir = "./data/sound"

    def load_config(self):
        pass

    def speak(self, text) -> str:
        # 此处应在start后调用
        # 拼接请求构成GET请求
        query = self.__url

        print(query)
        # 发送请求
        response = requests.get(
            query, params={"text": text, "text_language": "zh"}, timeout=5
        )

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
        root_path = "src/module/speaker/GSV/"
        program_path = "api.py"
        interpreter_path = "C:/Users/Student/anaconda3/envs/GSV/python.exe"

        command = [
            interpreter_path,
            program_path,
        ]

        subprocess.Popen(command, cwd=root_path, shell=True, env=os.environ)
