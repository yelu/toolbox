from s2s.Seq2SeqWithAttention import Seq2SeqWithAttention
import tensorflow as tf
import numpy as np
import unittest

if __name__ == "__main__":
    s2s = Seq2SeqWithAttention()
    s2s.Train(data_file = './cornell movie-dialogs corpus/train.small.tsv',
              model_file = './model/s2s',
              batch_size = 10,
              encoder_state_size = 128,
              decoder_state_size = 128,
              iteration = 2,
              verbose = True)

    loaded_s2s = Seq2SeqWithAttention()
    loaded_s2s.Load(model_file = './model/s2s')

    print(loaded_s2s.Predict("gosh , if only we could find kat a boyfriend ..."))
 
