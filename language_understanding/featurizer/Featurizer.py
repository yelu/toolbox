#!/usr/bin/env python

import os
import sys
import json
from shutil import copyfile
import pickle

class Featurizer(object):
    def __init__(self):
        self._featurizerMap = {}
        self._featurizerTopology = []
        self._outputNames = []
        self._featureIDMap = {}
        self._nextId = 0
        pass
    
    def AddFeaturizer(self, name, instance, inputs, export = True):
        self._featurizerMap[name] = {"instance":instance,\
                                   "inputs":inputs}
        self._featurizerTopology.append(name)
        if export:
            self._outputNames.append(name)

    def FitTransform(self, tokenizedQuery):
        variables = {}
        variables['tokenizedQuery'] = tokenizedQuery

        # get features from individual featurizers
        for ele in self._featurizerTopology:
            instance, inputNames = self._featurizerMap[ele]["instance"],\
                                   self._featurizerMap[ele]["inputs"]
            print(inputNames)
            print(instance)
            if isinstance(inputNames, list):
                inputs = []
                for inputName in inputNames:
                    inputs += variables[inputName]
            else:
                inputs = variables[inputNames]
            variables[ele] = instance.FitTransform(inputs)

        # allocate global id across all featurizers.
        ret = []
        for outputName in self._outputNames:
            features = variables[outputName]
            # allocate an id for features.
            for s,e,localFid in features:
                # check if out of boundary
                if s < 0 or e > len(tokenizedQuery) or e <= s:
                    continue
                globalFkey = (outputName, localFid)
                if globalFkey not in self._featureIDMap:
                    self._featureIDMap[globalFkey] = self._nextId
                    self._nextId += 1
                    if self._nextId > 2147483647:
                        raise "Feature count exceeds limits 2^31-1"
                if globalFkey in self._featureIDMap:
                    ret.append((e - 1, self._featureIDMap[globalFkey]))
        return ret

    def Transform(self, tokenizedQuery):
        variables = {}
        variables['tokenizedQuery'] = tokenizedQuery

        # get features from individual featurizers
        for ele in self._featurizerTopology:
            instance, inputNames = self._featurizerMap[ele]["instance"],\
                                   self._featurizerMap[ele]["inputs"]
            if isinstance(inputNames, list):
                inputs = []
                for inputName in inputNames:
                    inputs += variables[inputName]
            else:
                inputs = variables[inputNames]
            variables[ele] = instance.Transform(inputs)

        # allocate global id across all featurizers.
        ret = []
        for outputName in self._outputNames:
            features = variables[outputName]
            # lookup the id for features.
            for s,e,localFid in features:
                # check if out of boundary
                if s < 0 or e > len(tokenizedQuery) or e <= s:
                    continue
                globalFkey = (outputName, localFid)
                if globalFkey in self._featureIDMap:
                    ret.append((e - 1, self._featureIDMap[globalFkey]))
        return ret

    def Save(self, dstFile):
        dstDir = os.path.dirname(dstFile)
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)
        # copy dependent files of all featurizers.
        for _, featurizer in self._featurizerMap.items():
            instance = featurizer["instance"]
            if hasattr(instance, "dependentFiles"):
                newDependentFiles = []
                for dependentFile in instance.dependentFiles:
                    if dependentFile.startswith("self."):
                        p = dependentFile[5:]
                        srcDependentFile = getattr(instance, p)
                        setattr(instance, p, './' + os.path.basename(srcDependentFile))
                        newDependentFiles.append(dependentFile)
                    else:
                        srcDependentFile = dependentFile
                        newDependentFiles.append('./' + os.path.basename(srcDependentFile))
                    dstDependentFile = os.path.join(dstDir, 
                                                    os.path.basename(srcDependentFile))
                    copyfile(srcDependentFile, dstDependentFile)
                instance.dependentFiles = newDependentFiles
        with open(dstFile, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def Load(srcFile):
        srcFile = os.path.abspath(srcFile)
        srcDir = os.path.dirname(srcFile)
        cwd = os.getcwd()
        try:
            os.chdir(srcDir)
            with open(srcFile, 'rb') as f:
                featurizer = pickle.load(f)
            return featurizer
        finally:
            os.chdir(cwd)

