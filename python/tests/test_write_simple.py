import os

import tempfile

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

    nda_mono = read_wav_file(file_path, 0)
    with tempfile.NamedTemporaryFile() as tmp_file:
        write_wav_file(tmp_file.name, tmeta, nda_mono)

        nda_mono_readback = read_wav_file(tmp_file.name, 0)
        assert len(nda_mono) == len(nda_mono_readback)
        assert (nda_mono == nda_mono_readback).all()
