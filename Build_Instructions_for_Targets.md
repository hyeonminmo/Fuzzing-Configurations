# Build instructions for target C programs

## 1. bison-3.7
```
$ wget https://ftp.gnu.org/gnu/bison/bison-3.7.tar.xz
$ tar -xvf bison-3.7.tar.xz
$ cd bison-3.7
$ ./configure --prefix=/path/to/install/bison
$ make
$ make install
```
## 2. cflow-1.6
```
$ wget https://ftp.gnu.org/gnu/cflow/cflow-1.6.tar.xz
$ tar -xvf cflow-1.6.tar.xz
$ cd cflow-1.6
$ ./configure --prefix=/path/to/install/cflow
$ make
$ make install
```
## 3. binutils/nm 2.36.1
```
$ wget https://ftp.gnu.org/gnu/binutils/binutils-2.36.1.tar.xz
$ tar -xvf binutils-2.36.1.tar.xz
$ cd binutils-2.36.1
$ ./configure --enable-targets=all
$ make
```
## 4. binutils/size 2.36.1
```
$ wget https://ftp.gnu.org/gnu/binutils/binutils-2.36.1.tar.xz
$ tar -xvf binutils-2.36.1.tar.xz
$ cd binutils-2.36.1
$ ./configure --enable-targets=all
$ make
```
## 5. exiv2 0.27.2 
```
$ wget https://github.com/Exiv2/exiv2/releases/download/v0.27.2/exiv2-0.27.2-Source.tar.gz
$ tar -xvf exiv2-0.27.2-Source.tar.gz
$ cd exiv2-0.27.2-Source
$ mkdir build
$ cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$ cmake --build .
```
