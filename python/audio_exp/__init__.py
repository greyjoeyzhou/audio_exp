# import logging

from audio_exp._lowlevel import (
    read_wav_file_np,
    read_wav_file_metadata,
)

# FORMAT = "%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s"
# logging.basicConfig(format=FORMAT)
# logging.getLogger().setLevel(logging.INFO)

from typing import NamedTuple, TypeVar
import numpy as np
import numpy.typing as npt


class WavFileMeta(NamedTuple):
    bits_per_sample: int  # u16
    channels: int  # u16
    sample_rate: int  # u32
    sample_format_int: bool
    duration: int  # u32
    length: int  # u32
    duration_seconds: int  # u32


# TODO correctly type this
T = TypeVar("T", bound=np.int16)


def read_wav_file_metadata(file_path: str) -> WavFileMeta: ...
def read_wav_file_np(file_path: str, channel: int) -> npt.NDArray[T]: ...


__all__ = ["read_wav_file_metadata", "read_wav_file_np"]
