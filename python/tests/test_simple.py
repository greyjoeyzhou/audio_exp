import os
from audio_exp.audio_segment import AudioSegment

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

file_path = os.path.join(TEST_DIR, "StarWars3.wav")
as1 = AudioSegment.from_file(file_path)
print(as1)
