import os

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from datetime import datetime

from module.interface import BasicModule


class BasicSpeaker(BasicModule):
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

    def speak(self, text) -> str:
        if not os.path.exists(self.__output_dir):
            os.makedirs(self.__output_dir)

        # 生成语音文件名和路径
        file_name = self.__generate_filename()
        output_path = os.path.join(self.__output_dir, file_name)

        # 文件输出
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)

        # 创建语音合成器对象，设置语音合成的配置和输出
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        # 调用语音合成器进行语音合成，并获取合成结果
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

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
