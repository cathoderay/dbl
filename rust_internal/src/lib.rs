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
use std::path::Path;


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

fn create_database() -> () {
    // creates database if it doesn't exist

    let file_path = DATABASE_PATH.get().unwrap();
    let path = Path::new(&file_path);

    if !path.exists() {
        let file = File::create(&file_path);
        match file {
            Ok(f) => {
                println!("File {} created successfully: {:?}", file_path, f);
            },
            Err(e) => {
                eprintln!("Error creating file: {}", e);
            },
        }
    }
}

#[pyfunction]
fn build_index() -> () {
    create_database();
    let mut bytes_read = BYTES_READ_.lock().unwrap();

    let mut file = match File::open(DATABASE_PATH.get().unwrap()) {
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
    let key_value_separator = KEY_VALUE_SEPARATOR.get().unwrap();
    let delete_value = DELETE_VALUE.get().unwrap().chars().nth(0);
    for item in content.split(END_RECORD.get().unwrap()) {
        if item.is_empty() { continue; }
        let separator_index = item.find(key_value_separator).unwrap();
        let value_size: u64 = (item.len() - separator_index - 1) as u64;
        let key: String = item[0..separator_index].to_string();
        if item.chars().nth(separator_index + 1) == delete_value {
            index.remove(&key);
        }
        else {
            let value_start: u64 = current + (separator_index as u64) + 1;
            index.insert(key.clone(), IndexValue {start: value_start, size: value_size});
        }
        current += (item.len() as u64) + 1;
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
    create_database();
    Ok(())
}

#[pyfunction]
fn compact(
    compact_db_path:String,
) -> io::Result<()> {
    create_database();
    build_index();
    let index = INDEX_.lock().unwrap();

    let mut compact_file = match OpenOptions::new()
        .write(true)
        .create(true)
        .open(&compact_db_path) {
            Ok(f) => f,
            Err(e) => panic!("Failed to open compact file: {}", e)
    };

    let mut original_file = match File::open(DATABASE_PATH.get().unwrap()) {
        Ok(f) => f,
        Err(e) => panic!("Failed to open original file: {}", e),
    };

    for (key, value_data) in index.iter() {
        let mut buffer = vec![0; value_data.size.try_into().unwrap()];
        match original_file.seek(SeekFrom::Start(value_data.start)) {
            Ok(f) => f,
            Err(e) => panic!("Failed to seek original file: {}", e),
        };
        let _ = original_file.read_exact(&mut buffer);

        compact_file.write_all(&[
            key.as_bytes(),
            KEY_VALUE_SEPARATOR.get().unwrap().as_bytes(),
            &buffer,
            END_RECORD.get().unwrap().as_bytes()]
            .concat()
        )?;
    }

    Ok(())
}

#[pyfunction]
fn set(key: &[u8], value: &[u8]) -> io::Result<()> {
    let mut file = match OpenOptions::new()
        .append(true)
        .write(true)
        .create(true)
        .open(DATABASE_PATH.get().unwrap()) {
            Ok(f) => f,
            Err(e) => panic!("Failed to open file: {}", e)
    };

    file.write_all(&[
        key,
        KEY_VALUE_SEPARATOR.get().unwrap().as_bytes(),
        value,
        END_RECORD.get().unwrap().as_bytes()]
        .concat()
    )?;
    Ok(())
}

#[pyfunction]
fn get(py: Python<'_>, key: &[u8]) -> PyObject {
    create_database();
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

    let mut file = match File::open(DATABASE_PATH.get().unwrap()) {
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
fn get_index_keys() -> Vec<String> {
    let index = INDEX_.lock().unwrap();
    let keys: Vec<String> = index.keys().cloned().collect();
    keys
}

#[pyfunction]
fn clean_index() -> () {
    let mut index = INDEX_.lock().unwrap();
    index.clear();

    let mut bytes_read = BYTES_READ_.lock().unwrap();
    *bytes_read = 0;
}

#[pymodule]
fn rust_internal(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(initialize, m)?)?;
    m.add_function(wrap_pyfunction!(build_index, m)?)?;
    m.add_function(wrap_pyfunction!(set, m)?)?;
    m.add_function(wrap_pyfunction!(get, m)?)?;
    m.add_function(wrap_pyfunction!(get_bytes_read, m)?)?;
    m.add_function(wrap_pyfunction!(get_index_keys, m)?)?;
    m.add_function(wrap_pyfunction!(get_index_size, m)?)?;
    m.add_function(wrap_pyfunction!(clean_index, m)?)?;
    m.add_function(wrap_pyfunction!(compact, m)?)?;
    Ok(())
}
