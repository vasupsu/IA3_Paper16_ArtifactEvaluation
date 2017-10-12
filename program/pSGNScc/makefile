CXX = icpc
CC = icc

CPPFLAGS = -std=c++11 -qopenmp -O3 -D USE_MKL -mkl=sequential -Wall -xhost
CFLAGS = -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result

all: pSGNScc

pSGNScc: ../pSGNScc.cpp
	$(CXX) ../pSGNScc.cpp -o pSGNScc $(CPPFLAGS)
