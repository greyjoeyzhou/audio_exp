use pyo3::exceptions::PyValueError;

use log::info;

use hound;
use numpy::{IntoPyArray, PyArray1};
use pyo3::prelude::*;

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

#[pyfunction(name = "read_wav_file_metadata")]
fn read_wav_file_metadata(file_path: &str) -> PyResult<WavFileMeta> {
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

#[pyfunction]
fn read_wav_file_np<'py>(
    py: Python<'py>,
    file_path: &str,
    starting_time_ms: u32,
) -> PyResult<Bound<'py, PyArray1<i16>>> {
    info!("Reading WAV file: {}", file_path);
    let mut reader = hound::WavReader::open(file_path).unwrap();
    info!("reader created");
    let duration = reader.duration();
    let sample_rate = reader.spec().sample_rate;
    let starting_sample = starting_time_ms / 1000 * sample_rate;
    if starting_sample > duration {
        Err(PyErr::new::<PyValueError, _>(
            "Starting sample is beyond the duration of the WAV file",
        ))
    } else {
        reader.seek(starting_sample).unwrap();
        let samples: Vec<i16> = reader.samples::<i16>().map(|s| s.unwrap()).collect();
        Ok(samples.into_pyarray_bound(py))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_wav_file_np, m)?)?;
    m.add_function(wrap_pyfunction!(read_wav_file_metadata, m)?)?;
    Ok(())
}
