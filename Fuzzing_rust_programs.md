# Fuzzing Rust programs

## 0. Environment

- OS: ubuntu 20.04 LTS

## 1. Collect target programs

You can collect Rust programs from `crates.io`. Most crates in Rust provides source code repository.

![RustRepo](https://user-images.githubusercontent.com/3887348/167628770-d642ebfe-dd7c-4ab3-aa0a-9ac857d3e659.png "RustRepo")

For example, you can clone a repository as follows:
```
$ git clone https://github.com/rust-random/rand.git
```
Or, download a specific version as follows:
```
$ wget https://github.com/rust-random/rand/archive/refs/tags/0.8.5.tar.gz
$ tar -xvf 0.8.5.tar.gz
```

## 2. Fuzzing a Rust program

### 2-1. using cargo-fuzz

### 2-2. using afl.rs
