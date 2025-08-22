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


const DATABASE_PATH: &str = "/tmp/dbl.data";
const KEY_VALUE_SEPARATOR: char = ',';


fn build_index(bytes_read: u64) -> HashMap<String, IndexValue> {
    let mut file = match File::open(DATABASE_PATH) {
        Ok(f) => f,
        Err(e) => panic!("Failed to open file {}: {}", DATABASE_PATH, e),
    };

    match file.seek(SeekFrom::Start(bytes_read)) {
        Ok(f) => f,
        Err(e) => panic!("Failed to seek file {}: {}", DATABASE_PATH, e),
    };

    let mut content = String::new();
    match file.read_to_string(&mut content) {
        Ok(f) => f,
        Err(e) => panic!("Failed to read file {}: {}", DATABASE_PATH, e),
    };

    let mut index: HashMap<String, IndexValue> = HashMap::new();
    let mut current = bytes_read;
    for line in content.lines() {
        let separator_index = line.find(KEY_VALUE_SEPARATOR).unwrap();
        let value_size: u64 = (line.len() - separator_index - 1) as u64;
        let key: String = line[0..separator_index].to_string();
        let value_start: u64 = current + (separator_index as u64) + 1;
        index.insert(key.clone(), IndexValue {start: value_start, size: value_size});
        current += (line.len() as u64) + 1;
    }
    return index;
}


fn main() {
    let index: HashMap<String, IndexValue>;
    let bytes_read: u64 = 0u64;
    index = build_index(bytes_read);
    for (key, value) in &index {
        println!("{key} => {value}");
    }
}
