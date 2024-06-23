import os

from audio_exp.audio_segment import (
    AudioSegment,
    read_wav_file_metadata,
    read_wav_file_np,
)

from .common import TEST_DIR


def test_read_wav_file_single_channel():
    file_path = os.path.join(TEST_DIR, "StarWars3.wav")
    as1 = AudioSegment.from_file(file_path)
    as2 = read_wav_file_np(file_path, 0)
    tmeta = read_wav_file_metadata(file_path)
    assert len(as1._data) == len(as2)
    print(tmeta)


def test_read_wav_file_stereo_channel():
    file_path = os.path.join(TEST_DIR, "44100_pcm16_stereo.wav")
    as1 = AudioSegment.from_file(file_path)

    as2 = read_wav_file_np(file_path, 0)
    assert len(as1._data) == len(as2)

    tmeta = read_wav_file_metadata(file_path)
    assert as1.channels == tmeta.channels


# TODO
# surround sound
# pcm08, pcm24, pcm32
