# Fuzzing C programs with Persistent mode 

## 0. Environment

- OS: ubuntu 20.04 LTS

## 1. Install and build llvm and clang

### 1-1. Install llvm-11 and clang-11 from ubuntu package manager (apt)

```
$ sudo apt-get update
$ sudo apt-get install -y build-essential python3-dev automake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools
$ sudo apt-get install -y lld-11 llvm-11 llvm-11-dev clang-11
$ sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-dev
$ sudo apt-get install -y ninja-build
```

### 1-2. Download and build llvm-13 and clang-13

```
$ sudo apt install binutils-dev
$ wget https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-13.0.1.tar.gz
$ tar -xvf llvmorg-13.0.1.tar.gz
$ cd llvm-project-llvmorg-13.0.1
$ mkdir build
$ cd build
$ cmake \
    -DCLANG_INCLUDE_DOCS="OFF" \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_BINUTILS_INCDIR=/usr/include/ \
    -DLLVM_BUILD_LLVM_DYLIB="ON" \
    -DLLVM_ENABLE_BINDINGS="OFF" \
    -DLLVM_ENABLE_PROJECTS='clang;compiler-rt;libcxx;libcxxabi;libunwind;lld' \
    -DLLVM_ENABLE_WARNINGS="OFF" \
    -DLLVM_INCLUDE_BENCHMARKS="OFF" \
    -DLLVM_INCLUDE_DOCS="OFF" \
    -DLLVM_INCLUDE_EXAMPLES="OFF" \
    -DLLVM_INCLUDE_TESTS="OFF" \
    -DLLVM_LINK_LLVM_DYLIB="ON" \
    -DLLVM_TARGETS_TO_BUILD="host" \
    ../llvm/
$ cmake --build . -j4
```

## 2. Download and build AFL++ 4.00c

```
$ wget https://github.com/AFLplusplus/AFLplusplus/archive/refs/tags/4.00c.tar.gz
$ tar -xvf 4.00c.tar.gz
$ cd AFLplusplus-4.00c
if use llvm-11 (clang-11):
    $ LLVM_CONFIG=llvm-config-11 make distrib
else if use llvm-13 (clang-13):
    $ export PATH="/path/to/llvm13/bin:$PATH"
    $ export LLVM_CONFIG="/path/to/llvm13/bin/llvm-config"
    $ export LD_LIBRARY_PATH="$(llvm-config --libdir)${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    $ make distrib
```

## 3. Fuzzing with AFL++ using persistent mode

### 3-1. Build a target program

```
$ cd /path/to/a/target/program/
$ vim /path/to/main/file
--------------------------------------
//modify the main file as follows
+int main(int argc, char** argv){
+  while(__AFL_LOOP(10000)){
+    old_main(argc,argv);
+  }
+}

-int main(int argc, char** argv){
+int old_main(int argc, char** argv){
--------------------------------------
if use LLVM-PCGUARD mode (llvm-11):    
    $ CC=/path/to/afl/afl-clang-fast CXX=/path/to/afl/afl-clang-fast++ ./configure [...options...]
else if use LTO-PCGUARD (llvm-13, to support allow/deny list for instrumentation):
    $ CC=/path/to/afl/afl-clang-lto CXX=/path/to/afl/afl-clang-lto++ RANLIB=/path/to/llvm13/bin/llvm-ranlib AR=/path/to/llvm13/bin/llvm-ar ./configure [...options...]
$ make
```
NOTE: refer the [Build instructions for targets](Build_Instructions_for_Targets.md) to find details about build instructions for several target programs

### 3-2. Run fuzzing

```
$ mkdir fuzz
$ cp executable fuzz/
$ mkdir fuzz/in
$ cp /path/to/seed/inputs fuzz/in/
$ cd fuzz
$ sudo /path/to/afl/afl-system-config
$ /path/to/afl/afl-fuzz -i in/ -o out [..options..] -- ./executable @@
```
`executable` is the name of executable binary of the target program.

### 3-3. Failed running

1) Error message :
```
Hmm, your system is configured to send core dump notifications to an external utility. 
This will cause issues: there will be an extended delay between stumbling upon a crash and having this information relayed to the fuzzer via the standard waitpid() API.
    If you're just testing, set  'AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1'.
    To avoid having crashes misinterpreted as timeouts, please log in as root
    and temporarily modify /proc/sys/kernel/core_pattern, like so:
    echo core >/proc/sys/kernel/core_pattern
    ...
```
Solution :
```
$ sudo su 
$ echo core >/proc/sys/kernel/core_pattern 
$ exit 
```

2) Error message :
```
Whoops, your system uses on-demand CPU frequency scaling, adjusted between 2148 and 4964 MHz. 
Unfortunately, the scaling algorithm in the kernel is imperfect and can miss the short-lived processes spawned by  afl-fuzz. To keep things moving, run these commands as root:
...
```
Solution :
```
$ sudo su
$ cd /sys/devices/system/cpu
$ echo performance | tee cpu*/cpufreq/scaling_governor
$ exit
```


