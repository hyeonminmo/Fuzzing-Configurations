make clean
cp $1 $2
CFLAGS='-g -O0' ./configure --prefix=$3
