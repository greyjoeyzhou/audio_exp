import array
import wave

import numpy as np

from enum import IntEnum


class PCMEncoding(IntEnum):
    UNSIGNED_8 = 1
    SIGNED_16 = 2
    SIGNED_24 = 3
    SIGNED_32 = 4

    @property
    def max(self):
        return 255 if self == 1 else -self.min - 1

    @property
    def min(self):
        return 0 if self == 1 else -(2 ** (self.num_bits - 1))

    @property
    def num_bits(self):
        return 8 * self

    def decode(self, frames):
        match self:
            case PCMEncoding.UNSIGNED_8:
                # return np.frombuffer(frames, "u1") / self.max * 2 - 1
                return np.frombuffer(frames, "u1")
            case PCMEncoding.SIGNED_16:
                # The less-than symbol (<) in the format string explicitly
                # indicates little-endian as the byte order of
                # each two-byte audio sample (i2).
                # return np.frombuffer(frames, "<i2") / -self.min
                return np.frombuffer(frames, "<i2")
            case PCMEncoding.SIGNED_24:
                triplets = np.frombuffer(frames, "u1").reshape(-1, 3)
                padded = np.pad(triplets, ((0, 0), (0, 1)), mode="constant")
                samples = padded.flatten().view("<i4")
                samples[samples > self.max] += 2 * self.min
                return samples

                # The following code is an alternative less efficient implementation
                # samples = (
                #     int.from_bytes(frames[i : i + 3], byteorder="little", signed=True)
                #     for i in range(0, len(frames), 3)
                # )
                # return np.fromiter(samples, "<i4")
            case PCMEncoding.SIGNED_32:
                # return np.frombuffer(frames, "<i4") / -self.min
                return np.frombuffer(frames, "<i4")
            case _:
                raise TypeError("unsupported encoding")


class AudioSegment:
    def __init__(self, data=None, *args, **kwargs):
        """
        Initialize an AudioSegment object.

        Args:
            data (array.array or bytes or ndarray): The audio data.
            channels (int): The number of audio channels.
            sample_width (int): The sample width in bytes.
            frame_rate (int): The frame rate in Hz.
        """
        self.channels = kwargs.pop("channels", None)
        self.sample_width = kwargs.pop("sample_width", None)
        self.frame_rate = kwargs.pop("frame_rate", None)

        self.frame_width = self.channels * self.sample_width

        pcm = PCMEncoding(self.sample_width)

        # array aleady has type information
        # TODO maybe remove support for array.array
        if isinstance(data, array.array):
            data = np.array(data)

        elif isinstance(data, bytes):
            data = pcm.decode(data)
            # data = np.frombuffer(data, dtype="<h")
        elif isinstance(data, np.ndarray):
            pass

        self._data = data

    @classmethod
    def from_file(cls, file_path):
        # read audio data from a file into AudioSegment object
        # Tmperarily use wave module to read audio data

        with wave.open(file_path) as wav_file:
            metadata = wav_file.getparams()

            # the wave module merely returns the raw bytes
            # without providing any help in their interpretation.
            # temporarily read all frames
            frames = wav_file.readframes(metadata.nframes)

        obj = cls(
            data=frames,
            sample_width=metadata.sampwidth,
            frame_rate=metadata.framerate,
            channels=metadata.nchannels,
        )
        return obj

    def export(self, output_file_path):
        # export the AudioSegment to a new file
        # writing in binary mode
        with wave.open(output_file_path, mode="wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.sample_width)
            wav_file.setframerate(self.frame_rate)
            # writeframes() takes a bytes object as input
            # is there any overhead in converting the ndarray data to bytes?
            wav_file.writeframes(self._data)

    # Add more methods as needed
