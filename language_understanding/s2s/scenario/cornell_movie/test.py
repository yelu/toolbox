from s2s.Seq2SeqWithAttention import Seq2SeqWithAttention
import tensorflow as tf
import numpy as np
import unittest

if __name__ == "__main__":

    loaded_s2s = Seq2SeqWithAttention()
    loaded_s2s.Load(model_file = './model/s2s-0')
    vocabs = sorted(loaded_s2s.reader.vocabulary_count.items(), key = lambda x:x[1], reverse = True)[5000]
    for i in vocabs:
    	print(i)
    while(True):
        line = input(">")
        res = loaded_s2s.Predict(line.strip(), 4)
        print(res)
 
