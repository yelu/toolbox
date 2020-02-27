#!/usr/bin/env python

import os,sys
from DataReader import DataReader
import unittest

class TestDataReader(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Process(self):
        reader = DataReader()
        config, batches = reader.Read('./train.txt', 1, 7)
        print batches

if __name__ == "__main__":
    unittest.main()
