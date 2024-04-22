import array
import wave

import numpy as np


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

        if isinstance(data, array.array):
            data = data.tobytes()

        elif isinstance(data, bytes):
            # The less-than symbol (<) in the format string explicitly
            # indicates little-endian as the byte order of
            # each two-byte audio sample (h).
            data = np.frombuffer(data, dtype="<h")
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
