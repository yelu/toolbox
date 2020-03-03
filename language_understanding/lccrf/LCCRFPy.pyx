# distutils: language = c++
# distutils: sources = ./lccrf/c/lib_lccrf/Types.cpp ./lccrf/c/lib_lccrf/FWBW.cpp ./lccrf/c/lib_lccrf/Viterbi.cpp ./lccrf/c/lib_lccrf/LCCRF.cpp ./lccrf/c/lib_lccrf/SGDL1.cpp ./lccrf/c/lib_lccrf/MurmurHash3.cpp

from libcpp.list cimport list
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.map cimport map

cdef extern from "LCCRF.h":
    cdef cppclass LCCRF:
        LCCRF() except +
        void Fit(string&, int, double, double)
        vector[int] Predict(vector[pair[int, int]]&, int) except +
        vector[double]& GetWeights()
        void Save(string&)
        void Load(string&)

cdef class LCCRFPy:
    cdef LCCRF c_lccrf
    def __cinit__(self):
        self.c_lccrf = LCCRF()
    def Fit(self, dataFile, maxIteration = 1, learningRate = 0.001, variance = 0.001):
        self.c_lccrf.Fit(dataFile.encode('utf-8'), maxIteration, learningRate, variance)
    def Predict(self, x, length):
        y = self.c_lccrf.Predict(x, length)
        return y
    def GetWeights(self):
        return self.c_lccrf.GetWeights()
    def Save(self, weightsFile):
        self.c_lccrf.Save(weightsFile.encode('utf-8'))
    def Load(self, weightsFile):
        self.c_lccrf.Load(weightsFile.encode('utf-8'))

