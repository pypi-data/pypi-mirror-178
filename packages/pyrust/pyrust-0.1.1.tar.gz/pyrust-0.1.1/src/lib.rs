use pyo3::prelude::*;

/// Calculates the GC-content of a DNA sequence
#[pyfunction]
fn gc_content(dna: String) -> PyResult<f64> {
    let g: f64 = dna.matches('G').count() as f64;
    let c: f64 = dna.matches('C').count() as f64;
    let len: f64 = dna.len() as f64;
    Ok((g + c)/len)
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyrust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(gc_content, m)?)?;
    Ok(())
}
