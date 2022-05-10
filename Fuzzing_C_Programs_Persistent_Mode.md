0. Environment

OS: ubuntu 20.04 LTS

1. install and build llvm and clang

1-1. install llvm-11 and clang-11 from ubuntu package manager (apt)

$ sudo apt-get update
$ sudo apt-get install -y build-essential python3-dev automake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools
$ sudo apt-get install -y lld-11 llvm-11 llvm-11-dev clang-11
$ sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-dev
$ sudo apt-get install -y ninja-build

1-2. download and build llvm-13 and clang-13

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

2. download and build AFL++ 4.00c

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

3. Fuzzing with AFL++ using persistent mode

3-1. build a target program

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
NOTE: refer the file Build Instructions for Targets to find details about build instructions for several target programs

3-2. run fuzzing

$ mkdir fuzz
$ cp <excutable> fuzz/
$ mkdir fuzz/in
$ cp /path/to/seed/inputs fuzz/in/
$ cd fuzz
$ sudo /path/to/afl/afl-system-config
$ /path/to/afl/afl-fuzz -i in/ -o out [..options..] -- ./<excutable> @@

