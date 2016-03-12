
CFLAGS=-O2 -march=x86-64 -Wall -DNDEBUG -fPIC -pipe -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE
#CFLAGS=-g -Wall -fPIC


all: edf.o edflib.o
	gcc -shared obj/edflib.o obj/edf.o -lm -lssl -lcrypto -o lib/_edf.so


edf.o: recording/edf.c
	gcc recording/edf.c -c $(CFLAGS) -o obj/edf.o


edflib.o: recording/edflib.c
	gcc recording/edflib.c -c $(CFLAGS) -o obj/edflib.o


clean:
	rm obj/*.o *.pyc lib/*.so
