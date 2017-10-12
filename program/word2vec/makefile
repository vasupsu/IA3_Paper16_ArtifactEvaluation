CXX = icpc
CC = icc

OPT_FLAGS=-O3

CPPFLAGS = -std=c++11 -qopenmp $(OPT_FLAGS) -D USE_MKL -mkl=sequential -Wall -xhost
CFLAGS = -lm -pthread $(OPT_FLAGS) -march=native -Wall -funroll-loops

all: word2vec

word2vec: ../word2vec.c
	$(CC) ../word2vec.c -o word2vec $(CFLAGS)
