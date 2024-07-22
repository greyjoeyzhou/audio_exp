import os

from audio_exp._lowlevel import (
    read_wav_file_metadata,
    read_wav_file,
    write_wav_file,
)

from .common import TEST_DIR


def test_write_mono():
    file_path = os.path.join(TEST_DIR, "44100_pcm16_mono.wav")
    tmeta = read_wav_file_metadata(file_path)
    assert tmeta != None
    assert tmeta.bits_per_sample == 16
    assert tmeta.sample_rate == 44100
    assert tmeta.channels == 1
