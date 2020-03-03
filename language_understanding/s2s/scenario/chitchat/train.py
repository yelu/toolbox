from s2s.Seq2SeqWithAttention import Seq2SeqWithAttention
import tensorflow as tf
import numpy as np
import unittest

if __name__ == "__main__":
    s2s = Seq2SeqWithAttention()
    s2s.Train(data_file = './train.tsv',
              model_file = './model/s2s',
              batch_size = 64,
              encoder_state_size = 256,
              decoder_state_size = 256,
              dropout = 0.2,
              iteration = 100,
              verbose = True)

    loaded_s2s = Seq2SeqWithAttention()
    loaded_s2s.Load(model_file = './model/s2s')

    print(loaded_s2s.Predict("gosh , if only we could find kat a boyfriend ..."))
 
