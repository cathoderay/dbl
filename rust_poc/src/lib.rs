use pyo3::prelude::*;
use std::fs::File;
use std::io::Read;
use std::collections::HashMap;
use std::fmt;
use std::io::SeekFrom;
use std::io::Seek;


impl fmt::Display for IndexValue {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.start, self.size)
    }
}


struct IndexValue {
    start: u64,
    size: u64,
}


static DATABASE_PATH: once_cell::sync::OnceCell<String> = once_cell::sync::OnceCell::new();
static KEY_VALUE_SEPARATOR: once_cell::sync::OnceCell<String> = once_cell::sync::OnceCell::new();
static END_RECORD: once_cell::sync::OnceCell<String> = once_cell::sync::OnceCell::new();
static DELETE_VALUE: once_cell::sync::OnceCell<String> = once_cell::sync::OnceCell::new();


#[pyfunction]
fn build_index(bytes_read: u64) -> () {
    let mut file = match File::open(DATABASE_PATH.get().cloned().unwrap()) {
        Ok(f) => f,
        Err(e) => panic!("Failed to open file: {}", e),
    };

    match file.seek(SeekFrom::Start(bytes_read)) {
        Ok(f) => f,
        Err(e) => panic!("Failed to seek file: {}", e),
    };

    let mut content = String::new();
    match file.read_to_string(&mut content) {
        Ok(f) => f,
        Err(e) => panic!("Failed to read file: {}", e),
    };

    let mut index: HashMap<String, IndexValue> = HashMap::new();
    let mut current = bytes_read;
    for line in content.lines() {
        let separator_index = line.find(&KEY_VALUE_SEPARATOR.get().cloned().unwrap()).unwrap();
        let value_size: u64 = (line.len() - separator_index - 1) as u64;
        let key: String = line[0..separator_index].to_string();
        let value_start: u64 = current + (separator_index as u64) + 1;
        index.insert(key.clone(), IndexValue {start: value_start, size: value_size});
        current += (line.len() as u64) + 1;
    }
    for (key, value) in &index {
        println!("{key} => {value}");
    };
    // return index;
}

#[pyfunction]
fn initialize(
    database_path: String,
    key_value_separator: String,
    end_record: String,
    delete_value: String,
) -> PyResult<()> {
    DATABASE_PATH.set(database_path).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to set database path: {:?}", e))
    })?;
    KEY_VALUE_SEPARATOR.set(key_value_separator).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to set key value separator: {:?}", e))
    })?;
    END_RECORD.set(end_record).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to set end record: {:?}", e))
    })?;
    DELETE_VALUE.set(delete_value).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to set delete value: {:?}", e))
    })?;
    Ok(())
}


#[pymodule]
fn rust_poc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(initialize, m)?)?;
    m.add_function(wrap_pyfunction!(build_index, m)?)?;
    Ok(())
}
