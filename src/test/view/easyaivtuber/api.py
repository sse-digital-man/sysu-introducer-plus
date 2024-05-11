import sys
sys.path.append("./src")
from module.interface import manager


manager.load_modules()

module_dict = manager.info("view")
print(module_dict.to_dict())

view = manager.object("view")

# res = view.speak("D:/codefile/sysu-introducer-plus/data/audio/speech/uri_speech_0.wav")

# res = view.speak("D:/codefile/sysu-introducer-plus/data/audio/song/不分手的恋爱-汪苏泷_voice.MP3",
#                  "D:/codefile/sysu-introducer-plus/data/audio/song/不分手的恋爱-汪苏泷.MP3", mouth_offset=0.5, beat=2)

# res = view.background_music(
#     "D:/codefile/sysu-introducer-plus/data/audio/music/Noisy Radio - Chipi Chipi Chapa Chapa.flac")

res = view.stop_move()

print(res)
