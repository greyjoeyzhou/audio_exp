import os

from audio_exp.audio_segment import (
    AudioSegment,
    read_wav_file_metadata,
    read_wav_file_np,
)

from .common import TEST_DIR


def test_read_wav_file_metadata():
    file_path = os.path.join(TEST_DIR, "44100_pcm16_stereo.wav")
    tmeta = read_wav_file_metadata(file_path)
    assert tmeta != None
    assert tmeta.bits_per_sample == 16
    assert tmeta.sample_rate == 44100
    assert tmeta.channels == 2


def test_read_wav_file_single_channel():
    file_path = os.path.join(TEST_DIR, "StarWars3.wav")
    as1 = AudioSegment.from_file(file_path)
    as2 = read_wav_file_np(file_path, 0)
    assert as2 is not None
    assert len(as1._data) == len(as2)


def test_read_wav_file_stereo_channel():
    file_path = os.path.join(TEST_DIR, "44100_pcm16_stereo.wav")
    as1 = AudioSegment.from_file(file_path)

    as2 = read_wav_file_np(file_path, 0)
    assert as2 is not None
    assert len(as1._data) == len(as2)


# TODO
# surround sound
# pcm08, pcm24, pcm32
