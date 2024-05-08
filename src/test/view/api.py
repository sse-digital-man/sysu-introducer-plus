import sys
sys.path.append("./src")
from module.view import view

# res = view.speack("D:/codefile/sysu-introducer-plus/data/audio/speech/uri_speech_0.wav")

# res = view.sing("D:/codefile/sysu-introducer-plus/data/audio/song/不分手的恋爱-汪苏泷.MP3", "D:/codefile/sysu-introducer-plus/data/audio/song/不分手的恋爱-汪苏泷_voice.MP3", mouth_offset=0.5, beat=2)

# res = view.swing(
    # "D:/codefile/sysu-introducer-plus/data/audio/music/Noisy Radio - Chipi Chipi Chapa Chapa.flac")
    
res = view.stop_move()

print(res)

# view.start()
