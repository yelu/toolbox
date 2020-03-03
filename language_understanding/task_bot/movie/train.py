#!/usr/bin/env python

import os,sys
import json
from intent.IntentCNN import IntentCNN
from slot.SlotLCCRF import SlotLCCRF
import unittest

if __name__ == "__main__":

    train_data_file = './data/train.tsv'
    
    # train intent model
    cnn = IntentCNN()
    cnn.Train(train_file = train_data_file, 
                  query_col = 'query',
                  label_col = 'intent',
                  aux_cols = ['pre_intent:enum'],
                  work_dir = './intent_output/', 
                  iteration = 10,
                  max_token = 60, 
                  batch_size = 64,
                  embedding_dim = 128,
                  filter_sizes = [3, 4, 5], 
                  channel = 128,
                  verbose = True)
    
    loaded_cnn = IntentCNN()
    loaded_cnn.Load('./intent_output/model/model.ckpt')
    
    tp, total = loaded_cnn.Test(test_file = train_data_file,
             aux_cols = ['pre_intent:enum'],
    )
    print((tp, total))
    
    # train slot model
    tagger = SlotLCCRF()
    tagger.Train(data_file = train_data_file,
                 work_dir = './slot_output/',
                 query_col = 'slot_xml',
                 iteration = 100, 
                 learning_rate = 0.05, 
                 variance = 0.0008,
                 cfg_grammars = ['./data/cfg.xml'])

    loaded_tagger = SlotLCCRF()
    loaded_tagger.Load('./slot_output/model/')

    #test on training set.
    stat = loaded_tagger.Test(test_data = train_data_file,
                              query_col = 'slot_xml')
    print(json.dumps(stat, indent=4))

