# Fuzzing Rust programs

## 0. Environment

- OS: ubuntu 20.04 LTS
- claxon-0.4.1 as an example target program

### 0-1. Install Rust nightly version
```
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
$ source $HOME/.cargo/env
$ rustup toolchain install nightly
$ rustup default nightly
```

## 1. Collect target programs

You can collect Rust programs from `crates.io`. Most crates in Rust provides source code repository.

![RustRepo](https://user-images.githubusercontent.com/3887348/167628770-d642ebfe-dd7c-4ab3-aa0a-9ac857d3e659.png "RustRepo")

For example, you can clone a repository (claxon) as follows:
```
$ git clone https://github.com/ruuda/claxon.git
```
Or, download a specific version (claxon-0.4.1) as follows:
```
$ wget https://github.com/ruuda/claxon/archive/refs/tags/v0.4.1.tar.gz
$ tar -xvf v0.4.1.tar.gz
```

## 2. Install fuzzers for Rust

There are two available fuzzers for Rust, cargo-fuzz and afl.rs.

For cargo-fuzz,
```
$ cargo install cargo-fuzz
```

For afl.rs,
```
$ cargo install afl
```

## 2. Fuzzing a Rust program

### 2-1. using cargo-fuzz

#### 2-1-1. Fuzz target generation

For a Rust crate, you should create a fuzz target by follows:
```
$ cd /path/to/the/crate
$ cargo fuzz init
$ vim fuzz/fuzz_targets/fuzz_target_1.rs
---------------------------------
 #![no_main]
 #[macro_use] extern crate libfuzzer_sys;

 fuzz_target!(|data: &[u8]| {
+  // call fuzz target library functions here!
 });
---------------------------------
```

For some Rust crate such as claxon, the crate provide fuzz targets.
```
$ cd /path/to/the/claxon
$ cargo fuzz list
decode_full
decode_header
decode_single_block
diff
```
It shows the list of fuzz target names. You can also find source code of fuzz targets in `fuzz/fuzzers/`.

#### 2-1-2. Run fuzzing
```
cargo fuzz run decode_full
```
`decode_full` is a fuzz target name which is shown in the list.

### 2-2. using afl.rs

#### 2-2-1. Fuzz target generation
```
$ cd /path/to/the/claxon
$ vim Cargo.toml
----------------------------
// add the following lines
+ [dependencies]
+ afl="*"
----------------------------
$ mkdir src/bin
$ vim src/bin/fuzz_target.rs
----------------------------
// edit the file as the following lines
#[macro_use]
extern crate afl;
extern crate claxon;

use std::io::Cursor;

fn main() {
    fuzz!(|data: &[u8]| {
        let cursor = Cursor::new(data);
        let mut reader = match claxon::FlacReader::new(cursor) {
            Ok(r) => r,
            Err(..) => return,
        };

        for sample in reader.samples() {
            match sample {
                Ok(..) => { }
                Err(..) => return,
            }
        }
    });
}
----------------------------
```

#### 2-2-2. Run fuzzing
```
cargo afl build
mkdir in
cp /path/to/seed/inputs in/
cargo afl fuzz -i in -o out target/debug/fuzz_target
```
