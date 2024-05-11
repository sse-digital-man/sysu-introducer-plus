import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from datetime import datetime

from module.interface import BasicModule


class BasicSpeaker(BasicModule):
    def __init__(self):
        super().__init__("speaker")
        self._load_config()
        self.file_name = None  # 初始化文件名和路径
        self.speech_file_path = None
        # TODO 找到合适的声音，考虑使用SSML来风格化
        self.speech_config.speech_synthesis_voice_name = 'zh-CN-XiaohanNeural'

    def _load_config(self):
        info = self._read_config()
        self.speech_config = speechsdk.SpeechConfig(
            subscription=info['ms_subscription_key'], region='eastasia')

    def speak(self, text, output_dir=r'.\speech') -> str:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 生成语音文件名和路径
        self.file_name = f'{datetime.now().strftime(
            "BasicSpeaker-%Y%m%d%H%M%S")}.wav'
        self.speech_file_path = os.path.join(output_dir, self.file_name)

        # 文件输出
        audio_config = speechsdk.audio.AudioOutputConfig(
            filename=self.speech_file_path)

        # 创建语音合成器对象，设置语音合成的配置和输出
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config)

        # 调用语音合成器进行语音合成，并获取合成结果
        speech_synthesis_result = speech_synthesizer.speak_text_async(
            text).get()

        # 根据合成结果的原因进行相应的处理
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            stream = AudioDataStream(speech_synthesis_result)
            stream.save_to_wav_file(self.speech_file_path)
            print(f"BasicSpeaker speak for text: {text}")
            print(f"File saved at: {self.speech_file_path}")
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(
                        cancellation_details.error_details))
                    print(
                        "Did you set the speech resource key and region values?")
        return self.speech_file_path
