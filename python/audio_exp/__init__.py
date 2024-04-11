import logging

from audio_exp._lowlevel import hello, read_wav_file

FORMAT = "%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.INFO)

__all__ = ["hello", "read_wav_file"]
