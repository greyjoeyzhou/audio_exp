import array
import wave

import numpy as np

from enum import IntEnum

try:
    import audioop
except ImportError:
    # py3.13+ would not have audioop
    from .legacy_compatible import pyaudioop as audioop

from audio_exp import read_wav_file, read_wav_file_metadata


def db_to_float(db, using_amplitude=True):
    """
    Converts the input db to a float, which represents the equivalent
    ratio in power.
    """
    db = float(db)
    if using_amplitude:
        return 10 ** (db / 20)
    else:  # using power
        return 10 ** (db / 10)


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
    def from_file(cls, file_path, start_time=0):
        # read audio data from a file into AudioSegment object
        # use `read_wav_file_metadata` from `lib.rs` to read audio metadata
        # use `read_wav_file_np` from `lib.rs` to read audio frames

        metadata = read_wav_file_metadata(file_path)
        sample_width = metadata.bits_per_sample // 8

        # TODO: support read frames by nframes
        frames = read_wav_file(file_path, start_time)

        obj = cls(
            data=frames,
            sample_width=sample_width,
            frame_rate=metadata.sample_rate,
            channels=metadata.channels,
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

    def __add__(self, arg):
        if isinstance(arg, AudioSegment):
            return self.append(arg, crossfade=0)
        else:
            return self.apply_gain(arg)

    def __sub__(self, arg):
        if isinstance(arg, AudioSegment):
            raise TypeError(
                "AudioSegment objects can't be subtracted from " "each other"
            )
        else:
            return self.apply_gain(-arg)

    def append(self, seg, crossfade=0):
        # sync metadata
        seg1, seg2 = AudioSegment._sync(self, seg)

        if not crossfade:
            return seg1._spawn(seg1._data + seg2._data)
        elif crossfade > len(self):
            raise ValueError(
                "Crossfade is longer than the original AudioSegment ({}ms > {}ms)".format(
                    crossfade, len(self)
                )
            )
        elif crossfade > len(seg):
            raise ValueError(
                "Crossfade is longer than the appended AudioSegment ({}ms > {}ms)".format(
                    crossfade, len(seg)
                )
            )
        else:
            raise NotImplementedError("Crossfade not implemented")
        # TODO: implement crossfade
        # xf = seg1[-crossfade:].fade(to_gain=-120, start=0, end=float("inf"))
        # xf *= seg2[:crossfade].fade(from_gain=-120, start=0, end=float("inf"))

        # output = BytesIO()

        # output.write(seg1[:-crossfade]._data)
        # output.write(xf._data)
        # output.write(seg2[crossfade:]._data)

        # output.seek(0)
        # obj = seg1._spawn(data=output)
        # output.close()
        # return obj

    def apply_gain(self, volume_change):
        return self._spawn(
            data=audioop.mul(
                self._data, self.sample_width, db_to_float(float(volume_change))
            )
        )

    @classmethod
    def _sync(cls, *segs):
        channels = max(seg.channels for seg in segs)
        sample_width = max(seg.sample_width for seg in segs)
        frame_rate = max(seg.frame_rate for seg in segs)

        return tuple(
            seg.set_channels(channels)
            .set_frame_rate(frame_rate)
            .set_sample_width(sample_width)
            for seg in segs
        )

    def _spawn(self, data, overrides={}):
        """
        Creates a new audio segment using the metadata from the current one
        and the data passed in. Should be used whenever an AudioSegment is
        being returned by an operation that would alters the current one,
        since AudioSegment objects are immutable.
        """
        metadata = {
            "channels": self.channels,
            "sample_width": self.sample_width,
            "frame_rate": self.frame_rate,
            "frame_width": self.frame_width,
        }
        metadata.update(overrides)
        return self.__class__(data, **metadata)

    def set_channels(self, channels):
        if channels == self.channels:
            return self

        if channels == 2 and self.channels == 1:
            # TODO: reimplementation of ratecv for ndarray
            fn = audioop.tostereo
            frame_width = self.frame_width * 2
            fac = 1
            converted = fn(self._data.tobytes(), self.sample_width, fac, fac)
        elif channels == 1 and self.channels == 2:
            # TODO: reimplementation of ratecv for ndarray
            fn = audioop.tomono
            frame_width = self.frame_width // 2
            fac = 0.5
            converted = fn(self._data.tobytes(), self.sample_width, fac, fac)
        elif channels == 1:
            raise NotImplemented
            # TODO
            # channels_data = [seg.get_array_of_samples() for seg in self.split_to_mono()]
            # frame_count = int(self.frame_count())
            # converted = array.array(
            #     channels_data[0].typecode, b"\0" * (frame_count * self.sample_width)
            # )
            # for raw_channel_data in channels_data:
            #     for i in range(frame_count):
            #         converted[i] += raw_channel_data[i] // self.channels
            # frame_width = self.frame_width // self.channels
        elif self.channels == 1:
            raise NotImplemented
            # TODO
            # dup_channels = [self for iChannel in range(channels)]
            # return AudioSegment.from_mono_audiosegments(*dup_channels)
        else:
            raise ValueError(
                "AudioSegment.set_channels only supports mono-to-multi channel and multi-to-mono channel conversion"
            )

        return self._spawn(
            data=converted, overrides={"channels": channels, "frame_width": frame_width}
        )

    def set_sample_width(self, sample_width):
        if sample_width == self.sample_width:
            return self

        frame_width = self.channels * sample_width

        return self._spawn(
            # TODO: reimplementation of ratecv for ndarray
            audioop.lin2lin(self._data.tobytes(), self.sample_width, sample_width),
            overrides={"sample_width": sample_width, "frame_width": frame_width},
        )

    def set_frame_rate(self, frame_rate):
        if frame_rate == self.frame_rate:
            return self

        if self._data:
            # TODO: reimplementation of ratecv for ndarray
            converted, _ = audioop.ratecv(
                self._data.tobytes(),
                self.sample_width,
                self.channels,
                self.frame_rate,
                frame_rate,
                None,
            )
        else:
            converted = self._data

        return self._spawn(data=converted, overrides={"frame_rate": frame_rate})

    # Add more methods as needed
