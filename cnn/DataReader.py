import os,sys
import json
import random
import numpy as np

class DataReader(object):
    
    def __init__(self):
        pass
    
    def Read(self, file_path, batch, max_token):
        batches = []
        lines = []
        with open(file_path, 'r') as f:
            config = json.loads(f.readline())
            config["classes"] = int(config["classes"])
            config["auxiliary_dim"] = int(config["auxiliary_dim"])
            config["vocab_size"] = int(config["vocab_size"])
            classes = config["classes"]
            auxiliary_dim = config["auxiliary_dim"]

            for line in f:
                trimed = line.strip()
                if len(trimed) == 0 or trimed[0] == "#" or trimed[0] == "/":
                    continue
                else:
                    lines.append(trimed)
        xs = []
        auxs = []
        ys = []
        i = 0
        # group it by 3
        samples = list(zip(*(iter(lines),) * 3))
        random.shuffle(samples)
        for word_line, aux_line, label_line in samples:
            if  i % batch == 0 and len(xs) != 0:
                batches.append((np.array(xs), np.array(auxs), np.array(ys)))
                xs = []
                auxs = []
                ys = []
            
            i += 1
            
            words_str = word_line.split(':')[1].strip().split() 
            query_words = list(map(int, words_str))
            if len(query_words) >= max_token:
                query_words = query_words[0:max_token]
            else:
                query_words.extend([0] * (max_token - len(query_words)))
            xs.append(query_words)

            auxiliary = [0.0] * auxiliary_dim
            if config["auxiliary_dim"] > 0:
                aux_feature = aux_line.split(':')[1].strip().split()                  
                for feature in aux_feature:
                    fid, fv = feature.split(',')
                    auxiliary[int(fid)] = float(fv)
            auxs.append(auxiliary)

            y = [0.0] * classes
            y[int(label_line.split(':')[1].strip())] = 1.0
            ys.append(y)

        # output the remaining.
        if len(xs) != 0:
            batches.append((np.array(xs), np.array(auxs), np.array(ys)))

        return (config, batches)
                    
