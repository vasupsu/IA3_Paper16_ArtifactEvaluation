CXX = icpc
CC = icc

OPT_FLAGS=-O3

CPPFLAGS = -std=c++11 -qopenmp $(OPT_FLAGS) -D USE_MKL -mkl=sequential -Wall -xhost
CFLAGS = -lm -pthread $(OPT_FLAGS) -march=native -Wall -funroll-loops -Wno-unused-result

all: pSGNScc

pSGNScc: ../pSGNScc.cpp
	$(CXX) ../pSGNScc.cpp -o pSGNScc $(CPPFLAGS)
