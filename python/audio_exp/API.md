# API Documentation

## AudioSegment()

`AudioSegment` objects are immutable, and support a number of operators.

Any operations that combine multiple `AudioSegment` objects in *any* way will first ensure that they have the same number of channels, frame rate, sample rate, bit depth, etc. When these things do not match, the lower quality sound is modified to match the quality of the higher quality sound so that quality is not lost: mono is converted to stereo, bit depth and frame rate/sample rate are increased as needed. 

```python
from pydub import AudioSegment
sound1 = AudioSegment.from_file("/path/to/sound.wav", format="wav")
sound2 = AudioSegment.from_file("/path/to/another_sound.wav", format="wav")

# sound1 6 dB louder, then 3.5 dB quieter
louder = sound1 + 6
quieter = sound1 - 3.5

# sound1, with sound2 appended
combined = sound1 + sound2

# sound1 repeated 3 times
repeated = sound1 * 3

# duration
duration_in_milliseconds = len(sound1)

# first 5 seconds of sound1
beginning = sound1[:5000]

# Advanced usage, if you have raw audio data:
sound = AudioSegment(
    # raw audio data (bytes)
    data=b'…',
    # 2 byte (16 bit) samples
    sample_width=2,
    # 44.1 kHz frame rate
    frame_rate=44100,
)
```

### AudioSegment(data=b'...')

`init` function, init AudioSegment from raw data frames without headers.

### AudioSegment(…).from_file()

Open an audio file as an `AudioSegment` instance and return it. there are also a number of wrappers provided for convenience, but you should probably just use this directly.

### AudioSegment(…).export()

Write the `AudioSegment` object to a file – returns a file handle of the output file (you don't have to do anything with it, though).

### AudioSegment(…).apply_gain(`gain`) /  operator +

Change the amplitude (generally, loudness) of the `AudioSegment`. Gain is specified in dB. This method is used internally by the `+` operator.

### AudioSegment(…).append()

Returns a new `AudioSegment`, created by appending another `AudioSegment` to this one (i.e., adding it to the end), Optionally using a crossfade. `AudioSegment(…).append()` is used internally when adding `AudioSegment` objects together with the `+` operator.

By default a 100ms (0.1 second) crossfade is used to eliminate pops and crackles.

```python
from pydub import AudioSegment
sound1 = AudioSegment.from_file("sound1.wav")
sound2 = AudioSegment.from_file("sound2.wav")

# default 100 ms crossfade
combined = sound1.append(sound2)

# 5000 ms crossfade
combined_with_5_sec_crossfade = sound1.append(sound2, crossfade=5000)

# no crossfade
no_crossfade1 = sound1.append(sound2, crossfade=0)

# no crossfade
no_crossfade2 = sound1 + sound2
```







### AudioSegment.empty()

Creates a zero-duration `AudioSegment`.

```python
from pydub import AudioSegment
empty = AudioSegment.empty()

len(empty) == 0
```

### AudioSegment.silent()

Creates a silent audiosegment, which can be used as a placeholder, spacer, or as a canvas to overlay other sounds on top of.

```python
from pydub import AudioSegment

ten_second_silence = AudioSegment.silent(duration=10000)
```

### AudioSegment(…).overlay()

Overlays an `AudioSegment` onto this one. In the resulting `AudioSegment` they will play simultaneously. If the overlaid `AudioSegment` is longer than this one, the result will be truncated (so the end of the overlaid sound will be cut off). The result is always the same length as this `AudioSegment` even when using the `loop`, and `times` keyword arguments.

Since `AudioSegment` objects are immutable, you can get around this by overlaying the shorter sound on the longer one, or by creating a silent `AudioSegment` with the appropriate duration, and overlaying both sounds on to that one.



### AudioSegment(…).fade()

A more general (more flexible) fade method. You may specify `start` and `end`, or one of the two along with duration (e.g., `start` and `duration`).