make clean
cp $1 $2
CC=~/AFLplusplus/afl-clang-lto CXX=~/AFLplusplus/afl-clang-lto++ LD=~/AFLplusplus/afl-ld-lto CFLAGS='-g -O0' ./configure --prefix=$3
