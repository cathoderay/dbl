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
    static ref INDEX: Arc<Mutex<HashMap<String, IndexValue>>> = {
        let map = HashMap::new();
        Arc::new(Mutex::new(map))
    };
}


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

    let mut _new_index = INDEX.lock().unwrap();
    let mut current = bytes_read;
    for line in content.lines() {
        let separator_index = line.find(&KEY_VALUE_SEPARATOR.get().cloned().unwrap()).unwrap();
        let value_size: u64 = (line.len() - separator_index - 1) as u64;
        let key: String = line[0..separator_index].to_string();
        let value_start: u64 = current + (separator_index as u64) + 1;
        _new_index.insert(key.clone(), IndexValue {start: value_start, size: value_size});
        current += (line.len() as u64) + 1;
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
    Ok(())
}

#[pyfunction]
fn get(key: &[u8]) ->  () {
    build_index(0u64);
    let mut _index = INDEX.lock().unwrap();

    let start: u64;
    let size: u64;

    if let Some(value_data) = &_index.get(&String::from_utf8(key.to_vec()).unwrap()) {
        start = value_data.start;
        size = value_data.size;
    } else {
        return
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

    // TODO: deliver back to python result as a [u8] with dynamic size
    println!("{}", String::from_utf8(buffer).unwrap());
}


#[pymodule]
fn rust_poc(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(initialize, m)?)?;
    m.add_function(wrap_pyfunction!(build_index, m)?)?;
    m.add_function(wrap_pyfunction!(set, m)?)?;
    m.add_function(wrap_pyfunction!(get, m)?)?;
    Ok(())
}
