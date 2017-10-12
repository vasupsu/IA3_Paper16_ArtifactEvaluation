CXX = icpc
CC = icc
MPICC = mpiicpc

OPT_FLAGS=-O3

CPPFLAGS = -std=c++11 -qopenmp -O3 -D USE_MKL -mkl=sequential -Wall -xhost
CFLAGS = -lm -pthread $(OPT_FLAGS) -march=native -Wall -funroll-loops -Wno-unused-result

all: pWord2Vec

pWord2Vec: ../pWord2Vec.cpp
	$(CXX) ../pWord2Vec.cpp -o pWord2Vec $(CPPFLAGS)
