#!/usr/bin/env python
import os
import argparse

class NGramFeaturizer(object):
    def __init__(self, n, addBosEos = False):
        self._n = n
        self._addBosEos = addBosEos
        self._ngrams = {}
        self._nextId = 0

    def FitTransform(self, tokenizedQuery):
        if self._addBosEos:
            tokenizedQuery.insert(0, "BOS")
            tokenizedQuery.append("EOS")
        if len(tokenizedQuery) != 0:
            for i in range(self._n - 1, len(tokenizedQuery)):
                ngram = " ".join(tokenizedQuery[i + 1 - self._n : i + 1])
                if ngram not in self._ngrams:
                    self._ngrams[ngram] = self._nextId
                    self._nextId += 1
        
        return self.Transform(tokenizedQuery)

    def Transform(self, tokenizedQuery):
        features = []
        if self._addBosEos:
            tokenizedQuery.insert(0, "BOS")
            tokenizedQuery.append("EOS")
        for i in range(self._n - 1, len(tokenizedQuery)):
            ngram = " ".join(tokenizedQuery[i + 1 - self._n : i + 1])
            if ngram in self._ngrams:
                features.append((i + 1 - self._n, i + 1, self._ngrams[ngram]))
        return features
