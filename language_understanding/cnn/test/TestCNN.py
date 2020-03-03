#!/usr/bin/env python

import os,sys
from cnn.CNN import CNN
import unittest

class TestCNN(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Process(self):
        cnn = CNN()
        cnn.Train('./train.txt', 
                  './model/model.ckpt', 
                  iteration = 100,
                  max_token = 7, 
                  batch_size = 2,
                  embedding_dim = 4,
                  filter_sizes = [3, 4, 5], 
                  channel = 128,
                  verbose = True)
        loaded_cnn = CNN()
        loaded_cnn.Load('./model/model.ckpt')
        tp, total = loaded_cnn.Test('train.txt')
        precision = float(tp) / float(total)
        self.assertAlmostEqual(precision, 1.0)

if __name__ == "__main__":
    unittest.main()
