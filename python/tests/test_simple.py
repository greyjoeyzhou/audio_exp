import os
from audio_exp.audio_segment import AudioSegment
from audio_exp import read_wav_file_np

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

file_path = os.path.join(TEST_DIR, "StarWars3.wav")
as1 = AudioSegment.from_file(file_path)
as2 = read_wav_file_np(file_path, 0)
assert len(as1._data) == len(as2)
