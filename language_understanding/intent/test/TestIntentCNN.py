#!/usr/bin/env python

import os,sys
from intent.IntentCNN import IntentCNN
import unittest

class TestIntentCNN(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Process(self):
        cnn = IntentCNN()
        train_file = './train.tsv'
        cnn.Train(train_file = train_file, 
                  aux_cols = ['pre_intent:enum'],
                  work_dir = './train_output/', 
                  iteration = 10,
                  max_token = 60, 
                  batch_size = 64,
                  embedding_dim = 128,
                  filter_sizes = [3, 4, 5], 
                  channel = 128,
                  verbose = True)

        loaded_cnn = IntentCNN()
        loaded_cnn.Load('./train_output/model/model.ckpt')

        # test predict
        res = loaded_cnn.Predict('is it going to snow today')
        self.assertEqual(res[0], 'question_weather')

        # test batch_test
        tp, total = loaded_cnn.Test(test_file = train_file,
                                    aux_cols = ['pre_intent:enum'],
                                    )
        self.assertEqual((tp, total), (40, 40))

if __name__ == "__main__":
    unittest.main()
