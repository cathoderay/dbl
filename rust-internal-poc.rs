use std::fs::File;
use std::io::Read;
use std::collections::HashMap;


use std::fmt;


impl fmt::Display for IndexValue {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}-{}", self.start, self.size)
    }
}


struct IndexValue {
    start: usize,
    size: usize,
}


fn build_index() -> HashMap<String, IndexValue> {
    let file_path = "/tmp/dbl.data";
    const KEY_VALUE_SEPARATOR:char = ',';

    let mut file = match File::open(file_path) {
        Ok(f) => f,
        Err(e) => panic!("Failed to open file {}: {}", file_path, e),
    };

    let mut content = String::new();
    match file.read_to_string(&mut content) {
        Ok(_) => {
            let mut index: HashMap<String, IndexValue> = HashMap::new();
            for line in content.lines() {
                let separator_index = line.find(KEY_VALUE_SEPARATOR).unwrap();
                let value_size = line.len() - separator_index - 1;
                let key = &line[0..separator_index];
                index.insert(key.to_string(), IndexValue {start: separator_index, size: value_size});
            }

            return index;
        },
        Err(e) => panic!("Failed to read file {}: {}", file_path, e),
    }
}


fn main() {
    let index: HashMap<String, IndexValue> = build_index();
    for (key, value) in &index {
        println!("{key} => {value}");
    }
}
