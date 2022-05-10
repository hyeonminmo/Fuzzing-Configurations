# Extracting variable edges

## 0. Environment

- ubuntu 20.04 LTS
- AFL++ LTO mode necessary (LLVM-11+)

![VarEdgeExtractionOverview](https://user-images.githubusercontent.com/3887348/167570455-6da1f08f-ee7e-468c-abf3-39f5ae4918ae.png "VarEdgeExtractionOverview")

## 1. Extract edge IDs

```
$ CC=/path/to/afl/afl-clang-lto CXX=/path/to/afl/afl-clang-lto++ RANLIB=/path/to/llvm-11+/bin/llvm-ranlib AR=/path/to/llvm-11+/bin/llvm-ar ./configure
$ export AFL_LLVM_DOCUMENT_IDS=edgeIDfile
$ make
```
The environment variable `AFL_LLVM_DOCUMENT_IDS` denotes which file is used to document edge ids and `edgeIDfile` denotes the name of the file.
It is recommanded to use full path for `edgeIDfile`.

## 2. 
