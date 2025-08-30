use pyo3::prelude::*;
use std::fs::File;
use std::io::Read;
use std::collections::HashMap;
use std::fmt;
use std::io::SeekFrom;
use std::io::Seek;
use std::fs::OpenOptions;
use std::io::{self, Write};
use lazy_static::lazy_static;
use std::sync::{Arc, Mutex};
use pyo3::types::PyBytes;


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


lazy_static! {
    static ref INDEX_: Arc<Mutex<HashMap<String, IndexValue>>> = {
        let map = HashMap::new();
        Arc::new(Mutex::new(map))
    };
}


lazy_static! {
    static ref BYTES_READ_: Arc<Mutex<u64>> = {
        let bytes_read = 0;
        Arc::new(Mutex::new(bytes_read))
    };
}


#[pyfunction]
fn build_index() -> () {
    let mut bytes_read = BYTES_READ_.lock().unwrap();

    let mut file = match File::open(DATABASE_PATH.get().cloned().unwrap()) {
        Ok(f) => f,
        Err(e) => panic!("Failed to open file: {}", e),
    };

    match file.seek(SeekFrom::Start(*bytes_read)) {
        Ok(f) => f,
        Err(e) => panic!("Failed to seek file: {}", e),
    };

    let mut content = String::new();
    match file.read_to_string(&mut content) {
        Ok(f) => f,
        Err(e) => panic!("Failed to read file: {}", e),
    };

    let mut index = INDEX_.lock().unwrap();
    let mut current = *bytes_read;
    for line in content.lines() {
        let separator_index = line.find(&KEY_VALUE_SEPARATOR.get().cloned().unwrap()).unwrap();
        let value_size: u64 = (line.len() - separator_index - 1) as u64;
        let key: String = line[0..separator_index].to_string();
        let value_start: u64 = current + (separator_index as u64) + 1;
        index.insert(key.clone(), IndexValue {start: value_start, size: value_size});
        current += (line.len() as u64) + 1;
        *bytes_read = current;
    }
}

#[pyfunction]
fn initialize(
    database_path: String,
    key_value_separator: String,
    end_record: String,
    delete_value: String,
) -> PyResult<()> {
    DATABASE_PATH.set(database_path).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to initialize database path: {:?}", e))
    })?;
    KEY_VALUE_SEPARATOR.set(key_value_separator).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to initialize key value separator: {:?}", e))
    })?;
    END_RECORD.set(end_record).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to initialize end record: {:?}", e))
    })?;
    DELETE_VALUE.set(delete_value).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to initialize delete value: {:?}", e))
    })?;
    Ok(())
}

#[pyfunction]
fn set(key: &[u8], value: &[u8]) -> io::Result<()> {
    let mut file = match OpenOptions::new()
        .append(true)
        .write(true)
        .open(DATABASE_PATH.get().cloned().unwrap()) {
            Ok(f) => f,
            Err(e) => panic!("Failed to open file: {}", e)
    };

    let mut buffer: Vec<u8> = Vec::new();
    let a: &[u8] = key;
    let binding = KEY_VALUE_SEPARATOR.get().cloned().unwrap();
    let b: &[u8] = (&binding).as_bytes();
    let c: &[u8] = value;
    let binding = END_RECORD.get().cloned().unwrap();
    let d: &[u8] = (&binding).as_bytes();

    buffer.extend_from_slice(a);
    buffer.extend_from_slice(b);
    buffer.extend_from_slice(c);
    buffer.extend_from_slice(d);
    file.write_all(&buffer)?;
    build_index();
    Ok(())
}

#[pyfunction]
fn get(py: Python<'_>, key: &[u8]) -> PyObject {
    build_index();
    let index = INDEX_.lock().unwrap();

    let start: u64;
    let size: u64;

    if let Some(value_data) = &index.get(&String::from_utf8(key.to_vec()).unwrap()) {
        start = value_data.start;
        size = value_data.size;
    } else {
        return PyBytes::new(py, &vec![0; 0]).into()
    }

    let mut file = match File::open(DATABASE_PATH.get().cloned().unwrap()) {
        Ok(f) => f,
        Err(e) => panic!("Failed to open file: {}", e),
    };

    match file.seek(SeekFrom::Start(start)) {
        Ok(f) => f,
        Err(e) => panic!("Failed to seek file: {}", e),
    };

    let mut buffer = vec![0; size.try_into().unwrap()];
    let _ = file.read_exact(&mut buffer);

    return PyBytes::new(py, &buffer).into()
}

#[pyfunction]
fn get_bytes_read() -> u64 {
    return *BYTES_READ_.lock().unwrap();
}

#[pyfunction]
fn get_index_size() -> u64 {
    return INDEX_.lock().unwrap().len().try_into().unwrap();
}

#[pyfunction]
fn clean_index() -> () {
    let mut index = INDEX_.lock().unwrap();
    index.clear();

    let mut bytes_read = BYTES_READ_.lock().unwrap();
    *bytes_read = 0;
}

#[pymodule]
fn rust_poc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(initialize, m)?)?;
    m.add_function(wrap_pyfunction!(build_index, m)?)?;
    m.add_function(wrap_pyfunction!(set, m)?)?;
    m.add_function(wrap_pyfunction!(get, m)?)?;
    m.add_function(wrap_pyfunction!(get_bytes_read, m)?)?;
    m.add_function(wrap_pyfunction!(get_index_size, m)?)?;
    m.add_function(wrap_pyfunction!(clean_index, m)?)?;
    Ok(())
}
