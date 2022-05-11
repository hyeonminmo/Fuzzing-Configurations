# Advanced extraction of global variables to reinitialize

## 0. Environment
- OS: ubuntu 20.04 LTS

## 1. Overview

![AdvExhReinitOverview](https://user-images.githubusercontent.com/3887348/167621236-19c4d543-e4be-47ea-af5e-8449d09319e3.png "AdvExhReinitOverview")

## 2. Extract variable edges and inputs (Pre-run: afl-fuzz with debug mode)

This step produces variable edges and variable inputs of a target program. An input is variable if a fuzzing run with the input produces variable edges. You can extract variable edges and inputs by follows:
```
$ mkdir fuzz
$ mkdir fuzz/in
$ cp /path/to/seed/inputs fuzz/in
$ cp fuzz_executable fuzz/
$ cd fuzz
$ export AFL_DEBUG=1
$ /path/to/afl/afl-fuzz -i in/ -o out -m none -d -E 5000 -- fuzz_executable @@
```
`fuzz_executable` is the executable binary of the target program compiled by AFL++.
The the numbers after `var_bytes` in the file `out/default/fuzzer_stats` contains variable edge IDs if variable inputs are detected during the fuzzing.
The number 5000 after `-E` parameter means the number of inputs executed in the fuzzing procedure. If a variable is not produced during the 5000 inputs, you can increase the number.
Or, you can reduce the number if a variable input is detected early.

## 3. Extract (real) variable edges and inputs (afl-fuzz with debug mode for each input)

If there are many variable edges that are variable regardless of what inputs are used (due to such as randomness), it is necessary to identify what variable inputs are "real" variable inputs that are variable regarding to what inputs are used.
This step produces the real variable edges and inputs.
For each variable input, run the fuzzing with debug mode by follows:
```
$ rm in/*
$ cp /path/to/the/variable/input in/
$ /path/to/afl/afl-fuzz -i in/ -o out -m none -d -E 1 -- fuzz_executable @@
```
Each run produces the variable edges at `var_bytes` in the file `out/default/fuzzer_stats`. If the produced variable edges are different from the edges in `VarEdgesIgnore` file, the variable input to produce the variable edges is a real variable input.

## 4. Do exhaustive reinitialization with the real variable edges and inputs

This step identifies global variables to reinitialize associated with the real variable edges and inputs. This step follows the [Extracting global variables to reinitialize](Extracting_GVs_to_Reinitialize.md) procedure. If a global variable is identified as necessary to reinitialize, add the global variable to the GV list to reinit and add the variable edges to the `VarEdgesIgnore` file to avoid duplication.
