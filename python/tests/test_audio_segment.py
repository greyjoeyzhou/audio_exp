import unittest
from audio_exp.audio_segment import AudioSegment


class AudioSegmentTest(unittest.TestCase):
    # def test_from_file(self):
    #     # Test if AudioSegment can be created from a file
    #     file_path = "./sounds/8000_pcm08_mono.wav"
    #     audio = AudioSegment.from_file(file_path)
    #     self.assertIsInstance(audio, AudioSegment)
    #     self.assertIsNotNone(audio._data)
    #     self.assertEqual(audio.channels, 1)
    #     self.assertEqual(audio.sample_width, 1)
    #     self.assertEqual(audio.frame_rate, 8000)

    # def test_export(self):
    #     # Test if AudioSegment can be exported to a file
    #     audio = AudioSegment(
    #         data=b"\x00\x01\x02\x03", channels=1, sample_width=1, frame_rate=8000
    #     )
    #     output_file_path = "./output.wav"
    #     audio.export(output_file_path)

    def test_add_append(self):
        # Test addition of two AudioSegments
        audio1 = AudioSegment(
            data=b"\x00\x01\x02\x03", channels=1, sample_width=2, frame_rate=16000
        )
        audio2 = AudioSegment(
            data=b"\x04\x05\x06\x07", channels=1, sample_width=2, frame_rate=16000
        )
        result = audio1 + audio2
        assert result.channels == 1
        assert result.sample_width == 2
        assert result.frame_rate == 16000
        # Assert that the result AudioSegment has the correct data and properties

    def test_append(self):
        # Test appending two AudioSegments
        audio1 = AudioSegment(
            data=b"\x00\x01\x02\x03", channels=1, sample_width=2, frame_rate=16000
        )
        audio2 = AudioSegment(
            data=b"\x04\x05\x06\x07", channels=1, sample_width=2, frame_rate=16000
        )
        result = audio1.append(audio2, crossfade=0)
        assert result.channels == 1
        assert result.sample_width == 2
        assert result.frame_rate == 16000
        # Assert that the audio1 has the correct data and properties after appending

    def test_add_apply_gain(self):
        # Test applying gain to an AudioSegment
        audio = AudioSegment(
            data=b"\x00\x01\x02\x03", channels=1, sample_width=2, frame_rate=16000
        )
        result = audio + 3
        assert result.channels == 1
        assert result.sample_width == 2
        assert result.frame_rate == 16000
        # Assert that the audio has the correct data and properties after applying gain

    def test_apply_gain(self):
        # Test applying gain to an AudioSegment
        audio = AudioSegment(
            data=b"\x00\x01\x02\x03", channels=1, sample_width=2, frame_rate=16000
        )
        result = audio.apply_gain(3)
        assert result.channels == 1
        assert result.sample_width == 2
        assert result.frame_rate == 16000
        # Assert that the audio has the correct data and properties after applying gain

    # Add more tests as needed
