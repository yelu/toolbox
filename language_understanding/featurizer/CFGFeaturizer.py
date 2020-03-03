#!/usr/bin/env python
import os
import json
import argparse
from cfgparser.CFGParserPy import CFGParserPy

class CFGFeaturizer(object):
    def __init__(self, grammarFile, dependentFiles = []):
        self.grammarFile = grammarFile
        self._cfgParser = CFGParserPy()
        self._cfgParser.LoadXml(self.grammarFile)
        self.dependentFiles = dependentFiles
        self.dependentFiles.append("self.grammarFile")
        self.dependentFiles += self._cfgParser.GetDependentFiles()

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_cfgParser"] = None
        return state
    
    def __setstate__(self, state):
        state["_cfgParser"] = CFGParserPy()
        state["_cfgParser"].LoadXml(state["grammarFile"])
        self.__dict__.update(state)

    def FitTransform(self, tokenizeQuery):
        return self.Transform(tokenizeQuery)

    def Transform(self, tokenizeQuery):
        matches = self._cfgParser.Parse(tokenizeQuery)
        output = []
        for name, poses in matches.items():
            output += [(pos[0], pos[1], name) for pos in poses]
        return sorted(output)
        
