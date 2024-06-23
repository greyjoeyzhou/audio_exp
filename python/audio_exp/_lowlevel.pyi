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
