use log::info;

use hound;
use numpy::{IntoPyArray, PyArray1};
use pyo3::prelude::*;

/*
use symphonia::core::codecs::{DecoderOptions, CODEC_TYPE_NULL};
use symphonia::core::errors::Error;
use symphonia::core::formats::FormatOptions;
use symphonia::core::io::MediaSourceStream;
use symphonia::core::io::MediaSourceStream;
use symphonia::core::meta::MetadataOptions;
use symphonia::core::probe::Hint;
*/

// a general pattern would be implemented pure rust functions
// then wrap as python functions by using pyo3's macros

/// Returns a greeting.
fn hello() -> String {
    return "Hello from audio-exp!".to_string();
}

/// Prints a message.
#[pyfunction(name = "hello")]
fn py_hello() -> PyResult<String> {
    Ok(hello().into())
}

/// Reads a WAV file and returns the samples as a Vec<i16> wrapped with PyResult.
#[pyfunction(name = "read_wav_file")]
fn read_wav_file(file_path: &str) -> PyResult<Vec<i16>> {
    info!("Reading WAV file: {}", file_path);
    let mut reader = hound::WavReader::open(file_path).unwrap();
    info!("reader created");
    let samples = reader.samples::<i16>().map(|s| s.unwrap()).collect();
    Ok(samples)
}

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
fn read_wav_file_np<'py>(py: Python<'py>, file_path: &str) -> PyResult<Bound<'py, PyArray1<i16>>> {
    info!("Reading WAV file: {}", file_path);
    let mut reader = hound::WavReader::open(file_path).unwrap();
    info!("reader created");
    let samples: Vec<i16> = reader.samples::<i16>().map(|s| s.unwrap()).collect();
    Ok(samples.into_pyarray_bound(py))
}

/*
fn read_mp3(file_path: &str) -> Vec<i16> {
    let src = std::fs::File::open(&file_path).expect("failed to open media");

    // Create the media source stream.
    let mss = MediaSourceStream::new(Box::new(src), Default::default());

    // Create a probe hint using the file's extension. [Optional]
    let mut hint = Hint::new();
    hint.with_extension("mp3");

    // Use the default options for metadata and format readers.
    let meta_opts: MetadataOptions = Default::default();
    let fmt_opts: FormatOptions = Default::default();

    //let samples = reader.samples().map(|s| s.unwrap()).collect();
    samples
}
*/

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_hello, m)?)?;
    m.add_function(wrap_pyfunction!(read_wav_file, m)?)?;
    m.add_function(wrap_pyfunction!(read_wav_file_np, m)?)?;
    m.add_function(wrap_pyfunction!(read_wav_file_metadata, m)?)?;
    Ok(())
}

// unittest could be written in the same rs file
// we could test non-python functions in rs
// for wrapped python functions, we should test them in python

#[cfg(test)]
mod tests {
    use crate::hello;

    #[test]
    fn test_hello() {
        assert_eq!(hello(), "Hello from audio-exp!");
    }
}
