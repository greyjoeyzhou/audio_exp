# AnyAudio API Documentation

## wave format

The WAV audio file format is a binary format that exhibits the following structure on disk:

[![The Structure of a WAV File](https://files.realpython.com/media/wavstructure2.d97f203196ef.png)](https://files.realpython.com/media/wavstructure2.d97f203196ef.png)The Structure of a WAV File

As you can see, a WAV file begins with a **header** comprised of metadata, which describes how to interpret the sequence of **audio frames** that follow. Each frame consists of **channels** that correspond to loudspeakers, such as left and right or front and rear.

## Open / AudioReader

### wave like read/write

```python
# our tmp name
import anyaudio

with anyaudio.open("short.wav") as wav_file:
    # AudioSegment object
    audio_segment = wav_file.read()
    
    # _wave_params = namedtuple('_wave_params', 'channels frame_rate sample_width')
    metadata = wav_file.getparams()
   
    # read raw data as array/ndarray/bytes
    frames = wav_file.readframes(n=100)

with anyaudio.open("output.wav", mode="wb") as wav_file:
    wav_file.writeframes(frames)
```

### pydub like read/write

```python
from anyaudio import AudioSegment

song = AudioSegment.from_file("short.wav")

ten_minutes = 10 * 60 * 1000
first_10_minutes = song[:ten_minutes]

first_10_minutes.export("short_10.wav", format="wav")

```

### scipy like

https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html

https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html

`scipy` provide functions for read/write.

probably pass this choice.

read:

```python
from scipy.io import wavfile
samplerate, data = wavfile.read(wav_fname)
```

write:

```python
from scipy.io.wavfile import write
import numpy as np
samplerate = 44100; fs = 100
t = np.linspace(0., 1., samplerate)
amplitude = np.iinfo(np.int16).max
data = amplitude * np.sin(2. * np.pi * fs * t)
write("example.wav", samplerate, data.astype(np.int16))
```



## AudioSegment

### `__init__()`

````python
__init__(self, data=None, *args, **kwargs)
```
Args:
    data (array.array or bytes or np.array): The raw audio data without headers.
    
    channels (int): The number of audio channels.
    sample_width (int): The sample width in bytes.
    frame_rate (int): The frame rate in Hz.
```
````

`wave` in python containing these metadata: `_wave_params(nchannels=1, sampwidth=2, framerate=16000, nframes=2648832, comptype='NONE', compname='not compressed')`

### from_file()

keep this method to read the whole audio into an `AudioSegment`

More advanced read can use `anyaudio.open` like:

```
```





### export()

keep this method to write the whole `AudioSegment` audio on disk.



