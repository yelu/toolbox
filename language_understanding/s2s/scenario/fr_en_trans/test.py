from s2s.Seq2SeqWithAttention import Seq2SeqWithAttention
import tensorflow as tf
import numpy as np
import unittest
import csv,json

if __name__ == "__main__":

    loaded_s2s = Seq2SeqWithAttention()
    loaded_s2s.Load(model_file = './model/s2s')
    with open("./data/train.tsv", 'r', encoding='utf-8') as f, \
         open("./test_res.json", 'w', encoding = "utf-8") as test_res_f:
        reader = csv.DictReader(f, delimiter='\t')       
        for i, row in enumerate(reader):
            res = {}
            src_seq = row["src_seq"].strip()
            tokenized_dst_seq = row["dst_seq"].strip().split()
            if len(tokenized_dst_seq) > loaded_s2s.max_token:
                tokenized_dst_seq = tokenized_dst_seq[0:loaded_s2s.max_token]
            dst_seq = " ".join(loaded_s2s.dst_seq_reader.Transform(tokenized_dst_seq, False, False)[2])
            tokenized_predicted_seqs = loaded_s2s.Predict(src_seq, 4)
            predicted_seqs = [" ".join(ele) for ele in tokenized_predicted_seqs]
            res = {"src_seq" : src_seq,
                   "dst_seq" : dst_seq,
                   "predicted_seqs" : predicted_seqs}          
            print(json.dumps(res, ensure_ascii=False), file=test_res_f)
            if i % 1 == 0:
                print(json.dumps(res, indent=4))
            
 
