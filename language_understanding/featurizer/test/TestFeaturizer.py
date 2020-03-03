#!/usr/bin/env python

import os,sys
from featurizer.Featurizer import Featurizer
from featurizer.NGramFeaturizer import NGramFeaturizer
from featurizer.CFGFeaturizer import CFGFeaturizer
import unittest

class TestCaseFeaturizer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Process(self):
        featurizer = Featurizer()

        bigram = NGramFeaturizer(2)
        featurizer.AddFeaturizer("2gram", bigram, "tokenizedQuery")
        cfg = CFGFeaturizer("./cfg.xml", dependentFiles = ['cfg.xml'])
        featurizer.AddFeaturizer("cfg", cfg, "tokenizedQuery")

        queryFile = "./query.txt"
        tokenizedQueries = []
        with open(queryFile) as f:
            for line in f:
                tokenizedQuery = line.strip().split()
                features = featurizer.FitTransform(tokenizedQuery)

        featurizer.Save('./saved/featurizer.p')

        loadedFeaturizer = Featurizer.Load('./saved/featurizer.p')
        features = loadedFeaturizer.Transform("what is the weather on september 8 2016".split())
        print(features)
        self.assertEqual(len(features), 7)
        self.assertEqual(features[0], (1, 2))
        self.assertEqual(features[1], (2, 3))
        self.assertEqual(features[2], (3, 4))
        self.assertEqual(features[3], (6, 8))
        self.assertEqual(features[4], (7, 9))
        self.assertEqual(features[5], (6, 10))
        self.assertEqual(features[6], (7, 11))

if __name__ == "__main__":
    unittest.main()
