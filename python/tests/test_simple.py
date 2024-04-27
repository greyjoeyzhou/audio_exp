import os
from audio_exp.audio_segment import AudioSegment

file_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data/StarWars3.wav"
)

as1 = AudioSegment.from_file(file_path)
print(as1)
