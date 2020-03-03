#!/usr/bin/env python

import os,sys
from slot.SlotLCCRF import SlotLCCRF
import unittest
import json

class TestSlotLCCRF(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Predict(self):
        train_data_file = './train.tsv'
        tagger = SlotLCCRF()
        tagger.Train(data_file = './train.tsv',
                     work_dir = './output/',
                     query_col = 'slot_xml',
                     iteration = 1000, 
                     learning_rate = 0.05, 
                     variance = 0.0008,
                     cfg_grammars = ['./cfg.xml'])

        loaded_tagger = SlotLCCRF()
        loaded_tagger.Load('./output/model/')

        #test on training set.
        stat = loaded_tagger.Test(test_data = './train.tsv',
                                  query_col = 'slot_xml')
        print(json.dumps(stat, indent = 4))
        self.assertEqual(stat["accuracy"], 1.0)

        y = loaded_tagger.Predict('wake me up at eight am')
        print(y)

if __name__ == "__main__":
    unittest.main()
    #test = TestCRFTagger()
    #test.test_Fit()
