from s2s.Seq2SeqWithAttention import Seq2SeqWithAttention
import tensorflow as tf
import numpy as np
import unittest
import readline

if __name__ == "__main__":

    loaded_s2s = Seq2SeqWithAttention()
    loaded_s2s.Load(model_file = './model/s2s')

    while(True):
        print("----")
        line = input("> ")
        res = loaded_s2s.Predict(line.strip(), 10)
        for ele in res:
            if ele[0] == "<GO>":
                ele = ele[1:]
            if ele[-1] == "<EOS>":
                ele = ele[0:-1]
            print(" ".join(ele))
 
