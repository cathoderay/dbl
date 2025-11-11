#!/bin/bash

cd dbl_internal
cargo build --release
mv ./target/release/libdbl_internal.dylib ../dbl_internal.so
