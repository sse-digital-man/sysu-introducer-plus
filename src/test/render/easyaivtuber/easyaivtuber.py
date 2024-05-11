import sys
import time
sys.path.append("./src")
from module.interface import manager

manager.load_modules()
renderer = manager.object("renderer")
module_dict = manager.info("renderer")
print(module_dict.to_dict())

renderer.start()

# 暂停10s
time.sleep(10)

res = renderer.speak("D:/codefile/sysu-introducer-plus/data/sound/BasicSpeaker-20240511144342.wav")
# res = renderer.speak("D:/codefile/sysu-introducer-plus/data/music/uri_speech_0.wav")
# res = renderer.speak("D:/codefile/sysu-introducer-plus/data/music/不分手的恋爱-汪苏泷_voice.MP3",
#                  "D:/codefile/sysu-introducer-plus/data/music/不分手的恋爱-汪苏泷.MP3", mouth_offset=0.5, beat=2)
# res = renderer.background_music(
#     "D:/codefile/sysu-introducer-plus/data/music/Noisy Radio - Chipi Chipi Chapa Chapa.flac")
# res = renderer.stop_move()

print(res)
