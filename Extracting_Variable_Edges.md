# Extracting variable edges

## 0. Environment

- ubuntu 20.04 LTS
- AFL++ LTO mode necessary (LLVM-11+)

## 1. Overview

![VarEdgeExtractionOverview](https://user-images.githubusercontent.com/3887348/167570455-6da1f08f-ee7e-468c-abf3-39f5ae4918ae.png "VarEdgeExtractionOverview")

## 2. Extract edge IDs

```
$ CC=/path/to/afl/afl-clang-lto CXX=/path/to/afl/afl-clang-lto++ CFLAGS=$CFLAGS+'-O0' RANLIB=/path/to/llvm-11+/bin/llvm-ranlib AR=/path/to/llvm-11+/bin/llvm-ar ./configure
$ export AFL_LLVM_DOCUMENT_IDS=edgeIDfile
$ make
```
The environment variable `AFL_LLVM_DOCUMENT_IDS` denotes which file is used to document edge ids and `edgeIDfile` denotes the name of the file.
It is recommanded to use full path for `edgeIDfile`.

## 3. afl-fuzz with debug mode

```
$ mkdir fuzz
$ mkdir fuzz/in
$ cp /path/to/seed/inputs fuzz/in
$ cp executable fuzz/
$ cd fuzz
$ export AFL_DEBUG=1
$ /path/to/afl/afl-fuzz -i in/ -o out -m none -d -E 5000 -- executable @@
```

`executable` is the executable binary of the target program.
The the numbers after `var_bytes` in the file `out/default/fuzzer_stats` contains variable edge IDs if variable inputs are detected during the fuzzing.

## 4. Extract function of variable edges

You should extract functions containing variable edges by manual. Given variable edge IDs in the file `out/default/fuzzer_stats`, you can find corresponding functions by searching the IDs in `edgeIDfile`.

## 5. Count edge hit of each function

You should extract edge hit count of the extracted function by manually execute target program with gdb. First, you should manually identify line number of each block (edge) of the target function. An example of counting edge hits of the `n` identified lines is as follows:
```
$ vim /path/to/the/file/with/main/function
-----------------------------------------
//modify the main file as follows
+int main(int argc, char** argv){
+  for(int i=0;i<8;i++){
+    old_main(argc,argv);
+  }
+}

-int main(int argc, char** argv){
+int old_main(int argc, char** argv){
-----------------------------------------
$ ./configure && make
$ gdb executable
(gdb) b old_main
(gdb) b targetfile:linenumber_1
Breakpoint 1 at 0x40686f: file xxx.c, line xxx.
(gdb) ignore 1 10000
Will ignore next 10000 crossings of breakpoint 1.
(gdb) b targetfile:linenumber_2
Breakpoint 2 at 0x40686f: file xxx.c, line xxx.
(gdb) ignore 2 10000
Will ignore next 10000 crossings of breakpoint 2.
...
(gdb) b targetfile:linenumber_n
Breakpoint n at 0x40686f: file xxx.c, line xxx.
(gdb) ignore n 10000
Will ignore next 10000 crossings of breakpoint n.
(gdb) run /path/to/an/input/file
Breakpoint 1, old_main (argc=2, argv=0x7fffffffdf68) at main.c:766
(gdb) info b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x000000000040686f in xxx at xxx.c:xxx
	breakpoint already hit 1 time
	ignore next 10000 hits
2       breakpoint     keep y   0x00000000004068670 in xxx at xxx.c:xxx
	ignore next 10000 hits
...
n       breakpoint     keep y   0x00000000004068682 in xxx at xxx.c:xxx
	ignore next 10000 hits
```
