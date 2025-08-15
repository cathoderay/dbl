#include<string>
#include<fstream>
#include <iostream>
#include <unordered_map>

extern "C" {
    std::unordered_map<std::string, std::pair<int, int>> dbl_index;
    int bytes_read = 0;
    std::string DATABASE_PATH;
    std::string KEY_VALUE_SEPARATOR;
    std::string END_RECORD;

    void initialize(const char* database_path, const char* key_value_separator, const char* end_record) {
        DATABASE_PATH = database_path;
        KEY_VALUE_SEPARATOR = key_value_separator;
        END_RECORD = end_record;
    }

    void build_index() {
        std::ifstream file(DATABASE_PATH);

        if (!file.is_open()) {
            std::cerr << "Error opening file!" << DATABASE_PATH << std::endl;
            return;
        }
        
        std::string line;
        int current = bytes_read;
        int separator_index = 0;
        int value_size;
        std::string key;
        std::string value;
        std::string l;
        int read = 0;

        file.seekg(bytes_read, std::ios::beg);

        while (std::getline(file, line)) {
            read += line.length();
            l = line;
            separator_index = l.find(KEY_VALUE_SEPARATOR);
            value_size = line.length() - separator_index - 1;
            key = line.substr(0, separator_index);
            dbl_index[key] = std::make_pair(current + separator_index + 1, value_size);
            current += line.length() + 1;
            bytes_read = current;
        }
        file.close();
    }

    void set(const char* key, const char* value) {
        std::ofstream file(DATABASE_PATH, std::ios::app);

        if (!file.is_open()) {
            std::cerr << "Error opening file!" << DATABASE_PATH << std::endl;
            return;
        }

        file << key << KEY_VALUE_SEPARATOR << value << END_RECORD; 
        file.close();
    }

    const char* get(const char* key) {
        build_index();

        std::pair<int, int> value_pair = dbl_index[key];
        int start = value_pair.first;
        int size = value_pair.second;

        if (!start) {
            return "";
        }

        std::ifstream file(DATABASE_PATH);

        if (!file.is_open()) {
            std::cerr << "Error opening file!" << std::endl;
            return "";
        }
        std::vector<char> buffer(size);
        file.seekg(start, std::ios::beg);
        file.read(buffer.data(), size);
        file.close();
        std::string value(buffer.data(), buffer.size());
        const char* value_b = value.c_str();
        return value_b;
    }

    void clean_index() {
        dbl_index.clear();
        bytes_read = 0;
    }
}
