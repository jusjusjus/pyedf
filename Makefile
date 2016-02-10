
CFLAGS=-O2 -march=x86-64 -fPIC -pipe -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE
#CFLAGS=-g -Wall -fPIC


all: edf.o edflib.o
	gcc -shared obj/edflib.o obj/edf.o -lm -lssl -lcrypto -o lib/_edf.so


edf.o: src/edf.c
	gcc src/edf.c -c $(CFLAGS) -o obj/edf.o


edflib.o: src/edflib.c
	gcc src/edflib.c -c $(CFLAGS) -o obj/edflib.o


clean:
	rm obj/*.o *.pyc lib/*.so
