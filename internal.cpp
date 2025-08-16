#include<string>
#include<fstream>
#include <iostream>
#include <unordered_map>
#include <chrono>


extern "C" {
    std::unordered_map<std::string, std::vector<long long int>> dbl_index;
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
        long long int current = bytes_read;
        int separator_index = 0;
        int value_size;
        std::string key;
        std::string value;
        std::string l;
        long long int read = 0;

        file.seekg(bytes_read, std::ios::beg);

        while (std::getline(file, line)) {
            read += line.length();
            l = line;
            separator_index = l.find(KEY_VALUE_SEPARATOR);
            value_size = line.length() - separator_index - 1;
            key = line.substr(0, separator_index);
            dbl_index[key] = {current + separator_index + 1, value_size};
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

        std::vector<long long int> value_pair = dbl_index[key];

        if (value_pair.size() != 2) {
            return "";
        }

        long long int start = value_pair[0];
        int size = value_pair[1];

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

int main() {
    // Uncomment below to profile / optimize functions above
    /*
    const char* db_path = "/tmp/dbl.data-test";
    const char* kv_separator = ",";
    const char* end_record = "\n";
    initialize(db_path, kv_separator, end_record);
    auto start_time = std::chrono::high_resolution_clock::now();
    build_index();
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    long long elapsed_time_us = duration.count(); // Elapsed time in microseconds
    std::cout << "Index built." << std::endl;
    std::cout << "Bytes read: " << bytes_read << std::endl;
    std::cout << "Spent: " << elapsed_time_us << std::endl;
    return 0;
    */
}