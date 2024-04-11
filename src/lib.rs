use log::info;

use hound;
use pyo3::prelude::*;

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
#[pyfunction]
fn read_wav_file(file_path: &str) -> PyResult<Vec<i16>> {
    info!("Reading WAV file: {}", file_path);
    let mut reader = hound::WavReader::open(file_path).unwrap();
    info!("reader created");
    let samples = reader.samples::<i16>().map(|s| s.unwrap()).collect();
    Ok(samples)
}

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_log::init();
    m.add_function(wrap_pyfunction!(py_hello, m)?)?;
    m.add_function(wrap_pyfunction!(read_wav_file, m)?)?;
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
