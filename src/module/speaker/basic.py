import os

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from datetime import datetime
from lxml import etree

from .interface import SpeakerInterface


class BasicSpeaker(SpeakerInterface):
    def __init__(self):
        super().__init__()

        self.__output_dir = "./data/sound"

    def load_config(self):
        info = self._read_config()
        self.speech_config = speechsdk.SpeechConfig(
            subscription=info["apiKey"], region="eastasia"
        )

        # TODO 找到合适的声音，考虑使用SSML来风格化
        self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaohanNeural"
        # TODO 筛选后合适的说话人和声音风格（后续可供控制器进行选择？）
        self.speech_synthesis_voice_name_list = [
            "zh-CN-XiaoyiNeural",
            "zh-CN-XiaomengNeural",
        ]
        self.speech_synthesis_voice_style_list = [
            "cheerful",
            "hopeful",
            "excited",
            "friendly",
            "gentle",
            "whispering",
        ]

    # TODO 添加选择说话人、声音风格以及风格强度的逻辑（目前仅支持默认）
    def _prepare_ssml(self, text: str) -> str:
        """准备用于风格化的SSML

        Args:
            text (str): 待转化文本

        Returns:
            str: ssml文件对应的字符串
        """
        namespace = {
            "xmlns": "http://www.w3.org/2001/10/synthesis",
            "mstts": "https://www.w3.org/2001/mstts",
        }
        # 解析XML文件
        tree = etree.parse(
            "data/ssml/ssml.xml", parser=etree.XMLParser(encoding="utf-8")
        )
        root = tree.getroot()

        # 修改name属性
        voice_element = root.find(".//xmlns:voice", namespaces=namespace)
        voice_element.attrib["name"] = "zh-CN-XiaoyiNeural"

        # 修改style和styledegree属性
        express_as_element = root.find(".//mstts:express-as", namespaces=namespace)
        express_as_element.attrib["style"] = "hopeful"
        express_as_element.attrib["styledegree"] = "2"

        # 修改mstts标签内的内容
        express_as_element.text = text

        # 保存修改后的XML文件
        tree.write("data/ssml/ssml.xml", encoding="utf-8", xml_declaration=False)

        # 获取修改后的XML内容字符串
        modified_ssml = etree.tostring(root, encoding="utf-8").decode("utf-8")
        return modified_ssml

    def speak(self, text) -> str:
        if not os.path.exists(self.__output_dir):
            os.makedirs(self.__output_dir)

        # 生成语音文件名和路径
        file_name = self._generate_filename()
        output_path = os.path.join(self.__output_dir, file_name)

        # 文件输出
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)

        # 创建语音合成器对象，设置语音合成的配置和输出
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        # 调用语音合成器进行语音合成，并获取合成结果
        # speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        # 使用ssml方式调用语音合成器进行语音合成，并获取合成结果
        ssml_str = self._prepare_ssml(text)
        speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_str).get()

        # 根据合成结果的原因进行相应的处理
        reason = speech_synthesis_result.reason

        if reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            stream = AudioDataStream(speech_synthesis_result)
            stream.save_to_wav_file(output_path)
            # print(f"BasicSpeaker speak for text: {text}")
            # print(f"File saved at: {self.speech_file_path}")

        elif reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            # print("Speech synthesis canceled: {}".format(cancellation_details.reason))

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    # print("Error details: {}".format(cancellation_details.error_details))
                    # print("Did you set the speech resource key and region values?")

                    # FIXME: raise exception instead of printing error directly
                    raise Exception()

        return output_path

    def __generate_filename(self) -> str:
        return datetime.now().strftime("BasicSpeaker-%Y%m%d%H%M%S") + ".wav"
