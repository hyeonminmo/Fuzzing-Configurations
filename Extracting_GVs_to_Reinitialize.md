# Extracting Global Variables to Reinitialize

## 0. Environment

- use ubuntu 20.04 LTS
- `target` is the binary excutable of the target program compiled normally.
- `fuzz_target` is the binary executable of the target program compiled by afl with persistent mode.

## 1. Overview

![VarstoReinitExtractionOverview](https://user-images.githubusercontent.com/3887348/167619107-4d6562ea-180b-41fe-9902-5cd1ed2bd1d7.png "VarstoReinitExtractionOverview")

## 2. Extract all global variables of a target program

```
$ cd /path/to/target/program/
$ ./configure
$ make
$ gdb target
(gdb) b old_main
(gdb) set logging file globalvars
(gdb) set logging on
(gdb) info variables
(gdb) quit
```

## 3. Extract variable input files

```
$ mkdir fuzz
$ cp fuzz_target fuzz/
$ cp globalvars fuzz/
$ cp /path/to/repository/VariableDiffDetector/* /path/to/target/program/fuzz
$ mkdir fuzz/in.temp
$ cd fuzz
$ cat "" >> VarEdgesIgnore
$ cat "" >> VarInputsFound
$ ./ExtractingVarInputs.sh target /path/to/variable/corpus/inputs/
```
NOTE: `VarInputsFound` file contains the variable input file names after the extraction.

## 4. Extract global variables to reinitialize

```
$ cp /a/variable/input/file/in/VarInputsFound/file ./ 
$ python3 VariableDiffDetector.py globalvars target /a/variable/input/file/in/VarInputsFound/file
```
NOTE: `foundvars` file contains the global variables to be reinitialized.

## 5. Exclude variable edges, global variables, and source files from the analysis

### 5-1. Exclude variable edges from the analysis

You can exclude edges from the analysis by adding the corresponding edgeID to the `VarEdgesIgnore` file.

### 5-2. Exclude global variables from the analysis

You can exclude global variables from the analysis by adding the signature of the global variables to the global list `EXCLUDES` of the `VariableDiffDetector.py` file.

### 5-3. Exclude some source files from the analysis

You can exclude some source files from the analysis by adding the file names to the global list `EXCLUDES_FILES` of the `VariableDiffDetector.py` file.
