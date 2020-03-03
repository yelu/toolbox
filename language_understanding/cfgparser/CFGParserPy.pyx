# distutils: language = c++
# distutils: sources = ./cfgparser/cfgparser/CFGParser.cpp ./cfgparser/cfgparser/NodeMatcher.cpp

from libcpp.list cimport list
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.map cimport map

cdef extern from "CFGParser.h":
    cdef cppclass CFGParser:
        CFGParser() except +
        void LoadXml(const string&)
        map[string, vector[pair[int, int]]] Parse(const vector[string]&, bool)
        vector[string] GetDependentFiles()

cdef class CFGParserPy:
    cdef CFGParser c_cfgparser
    def __cinit__(self):
        self.c_cfgparser = CFGParser()
    def LoadXml(self, filePath):
        self.c_cfgparser.LoadXml(filePath.encode('utf-8'))
    def Parse(self, tokenizedQuery, merge = True):
        tokenBytes = []
        for ele in tokenizedQuery:
            tokenBytes.append(ele.encode('utf-8'))
        cdef map[string, vector[pair[int, int]]] resBytes = self.c_cfgparser.Parse(tokenBytes, merge)
        resStr = {}
        for k, v in resBytes.items():
            resStr[k.decode('utf-8')] = v
        return resStr
    def GetDependentFiles(self):
        resBytes = self.c_cfgparser.GetDependentFiles()
        resStr = []
        for ele in resBytes:
            resStr.append(ele.decode('utf-8'))
        return resStr
