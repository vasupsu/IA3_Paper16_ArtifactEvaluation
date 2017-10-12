CXX = icpc
CC = icc

CPPFLAGS = -std=c++11 -qopenmp -O3 -D USE_MKL -mkl=sequential -Wall -xhost
CFLAGS = -lm -pthread -O3 -march=native -Wall -funroll-loops

all: word2vec

word2vec: ../word2vec.c
	$(CC) ../word2vec.c -o word2vec $(CFLAGS)
