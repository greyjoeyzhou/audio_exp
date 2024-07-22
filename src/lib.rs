use pyo3::exceptions::PyValueError;

use log::info;

use hound;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArrayDyn};
use pyo3::prelude::*;
//use symphonia::core::sample;

#[pyclass]
struct WavFileMeta {
    bits_per_sample: u16,
    channels: u16,
    sample_rate: u32,
    sample_format_int: bool,
    duration: u32,
    length: u32,
    duration_seconds: u32,
}

#[pymethods]
impl WavFileMeta {
    #[getter]
    fn bits_per_sample(&self) -> u16 {
        self.bits_per_sample
    }

    #[getter]
    fn channels(&self) -> u16 {
        self.channels
    }

    #[getter]
    fn sample_rate(&self) -> u32 {
        self.sample_rate
    }

    #[getter]
    fn sample_format_int(&self) -> bool {
        self.sample_format_int
    }

    #[getter]
    fn duration(&self) -> u32 {
        self.duration
    }

    #[getter]
    fn length(&self) -> u32 {
        self.length
    }

    #[getter]
    fn duration_seconds(&self) -> u32 {
        self.duration_seconds
    }

    fn __str__(&self) -> String {
        format!(
            "WavFileMeta(bits_per_sample={}, channels={}, sample_rate={}, sample_format_int={})",
            self.bits_per_sample, self.channels, self.sample_rate, self.sample_format_int
        )
    }
}

fn read_wav_file_metadata(file_path: &str) -> Result<WavFileMeta, hound::Error> {
    let reader = hound::WavReader::open(file_path).unwrap();
    let duration = reader.duration();
    let length = reader.len();
    let spec = reader.spec();
    Ok(WavFileMeta {
        bits_per_sample: spec.bits_per_sample,
        channels: spec.channels,
        sample_rate: spec.sample_rate,
        sample_format_int: spec.sample_format == hound::SampleFormat::Int,
        duration: duration,
        length: length,
        duration_seconds: duration / spec.sample_rate, //  TODO check if we should make it float
    })
}

#[pyfunction(name = "read_wav_file_metadata")]
fn py_read_wav_file_metadata(file_path: &str) -> PyResult<WavFileMeta> {
    Ok(read_wav_file_metadata(file_path).unwrap())
}

#[pyfunction(name = "read_wav_file")]
fn py_read_wav_file_np<'py>(
    py: Python<'py>,
    file_path: &str,
    starting_time_ms: u32,
) -> PyResult<Bound<'py, PyArray1<i16>>> {
    info!("Reading WAV file: {}", file_path);
    let mut reader = hound::WavReader::open(file_path).unwrap();
    info!("reader created");
    let duration = reader.duration();
    let sample_rate = reader.spec().sample_rate;
    let channel = reader.spec().channels;
    let starting_sample = starting_time_ms / 1000 * sample_rate;
    if starting_sample > duration {
        Err(PyErr::new::<PyValueError, _>(
            "Starting sample is beyond the duration of the WAV file",
        ))
    } else {
        reader.seek(starting_sample).unwrap();
        match channel {
            1 => {
                let samples: Vec<i16> = reader.samples::<i16>().map(|s| s.unwrap()).collect();
                Ok(samples.into_pyarray_bound(py))
            }
            2 => {
                // let samples: Vec<i16> = reader.samples::<i16, i16>().map(|s| s.unwrap()).collect();

                let samples1: Vec<i16> = reader.samples().map(|s| s.unwrap()).collect();
                Ok(PyArray1::from_vec_bound(py, samples1))
                //Ok(samples1.into_pyarray_bound(py))
            }
            _ => Err(PyErr::new::<PyValueError, _>(
                "Only mono and stereo channels are supported",
            )),
        }
    }
}

fn read_wav_file(file_path: &str) -> Result<Vec<i16>, hound::Error> {
    info!("Reading WAV file: {}", file_path);
    let mut reader = hound::WavReader::open(file_path).unwrap();
    info!("reader created");
    let duration = reader.duration();
    let sample_rate = reader.spec().sample_rate;
    let channel = reader.spec().channels;
    let samples: Vec<i16> = reader.samples::<i16>().map(|s| s.unwrap()).collect();
    info!("{:?}, {:?}, {:?}", channel, duration, sample_rate);
    Ok(samples)
}

#[pyfunction(name = "write_wav_file")]
fn py_write_wav_file_np<'py>(
    py: Python<'py>,
    file_path: &str,
    spec: &WavFileMeta,
    data: PyReadonlyArrayDyn<'py, i16>,
) -> PyResult<()> {
    info!("Writing WAV file: {}", file_path);
    let sample_format = if spec.sample_format_int {
        hound::SampleFormat::Int
    } else {
        hound::SampleFormat::Float
    };

    let wavspec = hound::WavSpec {
        bits_per_sample: spec.bits_per_sample,
        channels: spec.channels,
        sample_rate: spec.sample_rate,
        sample_format: sample_format,
    };
    let mut writer = hound::WavWriter::create(file_path, wavspec).unwrap();
    info!("writer created");

    data.as_array().iter().for_each(|s| {
        writer.write_sample(*s).unwrap();
    });

    writer.finalize().unwrap();

    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_read_wav_file_np, m)?)?;
    m.add_function(wrap_pyfunction!(py_read_wav_file_metadata, m)?)?;
    m.add_function(wrap_pyfunction!(py_write_wav_file_np, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::{read_wav_file, read_wav_file_metadata};

    #[test]
    fn test_read_wav_file() {
        let file_path = "./python/tests/sounds/StarWars3.wav";
        let sample = read_wav_file(file_path);
        assert_eq!(sample.is_ok(), true);

        let file_path = "./python/tests/sounds/44100_pcm16_stereo.wav";
        let tmeta = read_wav_file_metadata(file_path).unwrap();
        let sample = read_wav_file(file_path);
        assert_eq!(sample.is_ok(), true);
        match sample {
            Ok(samples) => {
                assert_eq!(
                    samples.len(),
                    (tmeta.duration as usize) * (tmeta.channels as usize)
                );
            }
            Err(_) => {
                assert_eq!(true, false);
            }
        }
    }

    #[test]
    fn test_read_wav_file_metadata() {
        let file_path = "./python/tests/sounds/44100_pcm16_stereo.wav";
        let tmeta = read_wav_file_metadata(file_path).unwrap();

        assert_eq!(tmeta.bits_per_sample, 16);
        assert_eq!(tmeta.channels, 2);
        assert_eq!(tmeta.sample_rate, 44100);

        let file_path = "./python/tests/sounds/8000_pcm32_surround.wav";
        let tmeta = read_wav_file_metadata(file_path).unwrap();

        assert_eq!(tmeta.bits_per_sample, 32);
        assert_eq!(tmeta.channels, 3);
        assert_eq!(tmeta.sample_rate, 8000);
    }
}
