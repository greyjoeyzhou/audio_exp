import array
import numpy as np


class AudioSegment:
    def __init__(self, data=None, *args, **kwargs):
        """
        Initialize an AudioSegment object.

        Args:
            data (array.array or bytes): The audio data.
            sample_width (int): The sample width in bytes.
            frame_rate (int): The frame rate in Hz.
            channels (int): The number of audio channels.

        Raises:
            Exception: If either all audio parameters or no parameter is specified.
            ValueError: If the data length is not a multiple of '(sample_width * channels)'.

        Notes:
            - If `data` is an `array.array` object, it will be converted to bytes.
            - If any of the audio parameters (`sample_width`, `frame_rate`, `channels`) are specified,
              all of them must be specified.
            - If `sample_width` is specified, the data length must be a multiple of `(sample_width * channels)`.
            - If `sample_width` is not specified, the `frame_width` will not be calculated and `_data` will be None.
            - TODO: Convert 24-bit audio to 32-bit audio.
              (stdlib audioop and array modules do not support 24-bit data)
        """
        self.sample_width = kwargs.pop("sample_width", None)
        self.frame_rate = kwargs.pop("frame_rate", None)
        self.channels = kwargs.pop("channels", None)

        audio_params = (self.sample_width, self.frame_rate, self.channels)

        # data here maybe the raw wave frames without the header
        if isinstance(data, array.array):
            try:
                data = data.tobytes()
            except:
                data = data.tostring()
        # numpy array?
        # if isinstance(data, np.array):
        #     try:
        #         data = data.tobytes()
        #     except:
        #         data = data.tostring()

        # wav object?
        # normal construction
        try:
            data = data if isinstance(data, (str, bytes)) else data.read()
        except OSError:
            d = b""
            reader = data.read(2**31 - 1)
            while reader:
                d += reader
                reader = data.read(2**31 - 1)
            data = d

        wav_data = read_wav_audio(data)
        if not wav_data:
            raise Exception("Couldn't read wav audio from data")

        self.channels = wav_data.channels
        self.sample_width = wav_data.bits_per_sample // 8
        self.frame_rate = wav_data.sample_rate
        self.frame_width = self.channels * self.sample_width
        self._data = wav_data.raw_data

        # convert from unsigned integers in wav
        # try:
        #     import audioop
        # except ImportError:
        #     import pyaudioop as audioop
        # if self.sample_width == 1:
        #     self._data = audioop.bias(self._data, 1, -128)

        # prevent partial specification of arguments
        if any(audio_params) and None in audio_params:
            raise Exception(
                "Either all audio parameters or no parameter must be specified"
            )
        # all arguments are given
        elif self.sample_width is not None:
            if len(data) % (self.sample_width * self.channels) != 0:
                raise ValueError(
                    "data length must be a multiple of '(sample_width * channels)'"
                )

            self.frame_width = self.channels * self.sample_width

        # TODO
        # Convert 24-bit audio to 32-bit audio.
        # (stdlib audioop and array modules do not support 24-bit data)

    @classmethod
    def from_file(cls, file_path):
        # Add code to read audio data from a file
        pass

    def export(self, output_file_path):
        # Add code to export the audio segment to a new file
        pass

    def __len__(self):
        """
        returns the length of this audio segment in milliseconds
        """
        pass
        # return round(1000 * (self.frame_count() / self.frame_rate))

    def __add__(self, arg):
        pass
        # if isinstance(arg, AudioSegment):
        #     return self.append(arg, crossfade=0)
        # else:
        #     return self.apply_gain(arg)

    def __sub__(self, arg):
        pass
        # if isinstance(arg, AudioSegment):
        #     raise TypeError(
        #         "AudioSegment objects can't be subtracted from " "each other"
        #     )
        # else:
        #     return self.apply_gain(-arg)

    def __mul__(self, arg):
        """
        If the argument is an AudioSegment, overlay the multiplied audio
        segment.

        If it's a number, just use the string multiply operation to repeat the
        audio.

        The following would return an AudioSegment that contains the
        audio of audio_seg eight times

        `audio_seg * 8`
        """
        pass
        # if isinstance(arg, AudioSegment):
        #     return self.overlay(arg, position=0, loop=True)
        # else:
        #     return self._spawn(data=self._data * arg)

    def __radd__(self, rarg):
        """
        Permit use of sum() builtin with an iterable of AudioSegments
        """
        pass
        # if rarg == 0:
        #     return self
        # raise TypeError("Gains must be the second addend after the " "AudioSegment")

    def __iter__(self):
        pass
        # return (self[i] for i in xrange(len(self)))

    # Add more methods as needed
