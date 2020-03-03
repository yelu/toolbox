import os,sys
import json
import random
import numpy as np
import csv

class DataReader(object):
    
    def __init__(self):
        pass
    
    def Load(self,
             data_file,            
             seq_col,
             max_token,
             top_ratio):
        self.vocabulary = {'<UNK>':0, '<EOS>':1, '<PAD>':2, '<GO>':3}
        self.vocabulary_count = {}
        self.tokenized_seqs = []
        self.max_token = max_token
        with open(data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')            
            for j, row in enumerate(reader):
                tokens = row[seq_col].lower().split()
                if len(tokens) == 0:
                    raise Exception("line %d : setentce empty. please remove it manully." % j)
                elif len(tokens) > max_token: 
                    tokens = tokens[:max_token]
                    print("line %d : setentce too long(>%d), truncated." % (j, max_token))
                self.tokenized_seqs.append(tokens)
                for token in tokens:
                    if token in self.vocabulary_count:
                        self.vocabulary_count[token] += 1
                    else:
                        self.vocabulary_count[token] = 1
        sorted_by_count = sorted(self.vocabulary_count.items(), key = lambda x:x[1], reverse=True)
        next_id = len(self.vocabulary)
        self.top_n = int(len(sorted_by_count) * top_ratio)
        print("total words:%d vocab_size:%d" % \
                (len(sorted_by_count), self.top_n))
        sorted_by_count = sorted_by_count[0:self.top_n]
        for word, count in sorted_by_count:
            if word not in self.vocabulary:
                self.vocabulary[word] = next_id
                next_id += 1
        self.id_to_word = dict((v,k) for k,v in self.vocabulary.items())
                
    def Read(self, batch_size, add_go, add_eos):
        for batch in DataReader.GroupByCount(self.tokenized_seqs, batch_size, True):
            vecs, masks = [], []
            padded_size = max(len(x) for x in batch)
            if add_go:
                padded_size += 1
            if add_eos:
                padded_size += 1
            for tokenized_seq in batch:
                vec, mask, _ = self.Transform(tokenized_seq, add_go, add_eos, padded_size)
                vecs.append(vec)
                masks.append(mask)
            yield (vecs, masks)
        
    def Transform(self, tokenized_seq, add_go = False, add_eos = False, padded_size = None):
        vec, mask, tokens = [], [], []
        for t in tokenized_seq:
            if t not in self.vocabulary:
                vec.append(self.vocabulary['<UNK>'])
                tokens.append('<UNK>')
                mask.append(1)
            else:
                vec.append(self.vocabulary[t])
                tokens.append(t)
                mask.append(1)
        if add_go:
            vec = [self.vocabulary['<GO>']] + vec
            tokens = ['<GO>'] + tokens
            mask.append(1)
        if add_eos:
            vec.append(self.vocabulary['<EOS>'])
            tokens.append('<EOS>')
            mask.append(1)
        if padded_size != None:
            vec += ([self.vocabulary['<PAD>']] * (padded_size - len(vec)))
            tokens += (['<PAD>'] * (len(vec) - len(mask)))
            mask += ([0] * (len(vec) - len(mask))) 
        return (vec, mask, tokens)

    def Lookup(self, ids):
        res = [self.id_to_word[i] if i in self.id_to_word else '<UNK>' for i in ids]
        return res
    
    def GetVocabularySize(self):
        return len(self.vocabulary)

    def GetGoSymbol(self):
        return self.vocabulary['<GO>']

    def GetEOSSymbol(self):
        return self.vocabulary['<EOS>']

    @staticmethod
    def GroupByCount(l, count, round = False):
        batch = []
        for ele in l:
            if len(batch) >= count:
                yield batch
                batch = []
            batch.append(ele)
        
        if len(batch) != 0:
            batch += l[0:count - len(batch)]
            yield batch
