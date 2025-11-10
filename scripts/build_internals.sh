#!/bin/bash

cd rust_internal
cargo build --release
mv ./target/release/librust_internal.dylib ../rust_internal.so
