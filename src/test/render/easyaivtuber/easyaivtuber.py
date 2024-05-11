import sys
import time
sys.path.append("./src")
from module.interface import manager

manager.load_modules()
render = manager.object("render")
module_dict = manager.info("render")
print(module_dict.to_dict())

render.start()

# 暂停10s
time.sleep(10)
# res = render.speak("D:/codefile/sysu-introducer-plus/data/sound/speech/uri_speech_0.wav")
# res = render.speak("D:/codefile/sysu-introducer-plus/data/sound/song/不分手的恋爱-汪苏泷_voice.MP3",
#                  "D:/codefile/sysu-introducer-plus/data/sound/song/不分手的恋爱-汪苏泷.MP3", mouth_offset=0.5, beat=2)
res = render.background_music(
    "D:/codefile/sysu-introducer-plus/data/sound/music/Noisy Radio - Chipi Chipi Chapa Chapa.flac")
# res = render.stop_move()
print(res)
