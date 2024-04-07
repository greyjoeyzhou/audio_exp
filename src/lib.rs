use hound;
use pyo3::prelude::*;

/// Prints a message.
#[pyfunction]
fn hello() -> PyResult<String> {
    Ok("Hello from audio-exp!".into())
}

/// Reads a WAV file and returns the samples as a Vec<i16> wrapped with PyResult.
#[pyfunction]
fn read_wav_file(file_path: &str) -> PyResult<Vec<i16>> {
    let mut reader = hound::WavReader::open(file_path).unwrap();
    let samples = reader.samples::<i16>().map(|s| s.unwrap()).collect();
    Ok(samples)
}

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(read_wav_file, m)?)?;
    Ok(())
}
