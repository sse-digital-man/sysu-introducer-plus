import os
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
        '''
        TODO: 使用DockerSDK for python 启动Docker容器提供服务
        手动启动命令如下：
        pull image: `docker pull kingkia/gpt-sovits-api`
        run: `docker run -it -d --gpus=all --shm-size="16G" --env=is_half=False -v=D:\GSV\GPT-SoVITS\output:/workspace/output -v=D:\GSV\GPT-SoVITS\logs:/workspace/logs -v=D:\GSV\GPT-SoVITS\SoVITS_weights:/workspace/SoVITS_weights -v=D:\GSV\GPT-SoVITS\GPT_weights:/workspace/GPT_weights -v=D:\GSV\GPT-SoVITS\reference:/workspace/reference -v=D:\GSV\GPT-SoVITS\config.py:/workspace/config.py -p 9880:9880 --name gpt-sovits-api kingkia/gpt-sovits-api`

        > 根据需要修改volume路径，必须写的包括SoVITS_weights、GPT_weights、reference以及config.py（可以通过配置来配置）
        > 需要修改config.py文件中的一些参数，如模型路径、参考音频路径、参考音频文字、参考语言等
        '''
        pass
