import numpy as np
import librosa

def generate_beat_data(music_path, beat=2):
    # 提取音频节奏
    # beat取值1，2，4，控制点头节奏速度
    if beat not in [1, 2, 4]:
        beat = 2
    y, sr = librosa.load(music_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_times = np.concatenate([[0], beat_times]).tolist()
    beat_times = [round(bt, 2) for bt in beat_times[::beat]]
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    frame_intervals = int(len(y) / len(onset_env))
    beat_strengths = np.array([np.max(y[i:i + frame_intervals]) for i in range(0, len(y), frame_intervals)])
    beat_strengths = np.clip(beat_strengths[beat_frames[::beat]], 0., 1.).tolist()
    return beat_times, beat_strengths


generate_beat_data("D:\\codefile\\sysu-introducer-plus\\src\\interface\\view\\data\\music\\Noisy Radio - Chipi Chipi Chapa Chapa.flac", beat=1)