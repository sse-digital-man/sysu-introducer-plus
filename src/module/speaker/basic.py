import os

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream

from .interface import SpeakerInterface


class BasicSpeaker(SpeakerInterface):
    def __init__(self):
        super().__init__()

        self.__output_dir = "./data/sound"
        self.__speech_config = None

        # self.__speech_synthesis_voice_name_list = [
        #     "zh-CN-XiaoyiNeural",
        #     "zh-CN-XiaomengNeural",
        # ]
        # self.__speech_synthesis_voice_style_list = [
        #     "cheerful",
        #     "hopeful",
        #     "excited",
        #     "friendly",
        #     "gentle",
        #     "whispering",
        # ]

    def load_config(self):
        info = self._read_config()
        self.__speech_config = speechsdk.SpeechConfig(
            subscription=info["apiKey"], region="eastasia"
        )

        self.__speech_config.speech_synthesis_voice_name = "zh-CN-XiaohanNeural"

        # TODO 筛选后合适的说话人和声音风格（后续可供控制器进行选择？）

    # TODO 添加选择说话人、声音风格以及风格强度的逻辑（目前仅支持默认）
    def _prepare_ssml(self, text: str) -> str:
        """准备用于风格化的SSML

        Args:
            text (str): 待转化文本

        Returns:
            str: ssml文件对应的字符串
        """

        # ssml 风格模版
        ssml = """
            <speak 
                xmlns="http://www.w3.org/2001/10/synthesis"
                xmlns:mstts="https://www.w3.org/2001/mstts"
                version="1.0" xml:lang="zh-CN"
            >
                <voice name="zh-CN-XiaoyiNeural">
                    <mstts:express-as style="hopeful" styledegree="2">{text}</mstts:express-as>
                </voice>
            </speak>
        """

        # 获取修改后的XML内容字符串
        return ssml.format(text=text)

    @SpeakerInterface._handle_log
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
            speech_config=self.__speech_config, audio_config=audio_config
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

        return os.path.join(os.getcwd(), output_path)
