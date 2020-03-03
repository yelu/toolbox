import os
import json
import csv
import numpy as np
import random
from shutil import copyfile
from cnn.CNN import CNN

class IntentCNN(object):

    def __init__(self):
        pass

    def _FitData(self, data_file, dst_dir,
                 query_col, label_col, aux_cols):
        # aux_cols contains some enum column, we will preprocess the data file
        aux_to_id = {}
        for aux_col in aux_cols:
            if aux_col.endswith(":enum"):
                aux_to_id[aux_col] = {}
            else:
                aux_to_id[aux_col] = 0
        reader = csv.DictReader(open(data_file, 'r'), delimiter='\t')
        for row in reader:
            for aux,_ in aux_to_id.items():
                if not aux.endswith(':enum'):
                    continue
                value = row[aux].strip()
                if value == '*':
                    continue
                aux_to_id[aux][value] = 0

        new_aux_to_id = {}
        aux_dim = 0
        for aux_name, v in aux_to_id.items():
            if type(v) is int:
                new_aux_to_id[aux_name] = aux_dim
                aux_dim += 1
            else:
                if len(v) == 0:
                    continue
                new_aux_to_id[aux_name] = {}
                for aux_value,_ in v.items():
                    new_aux_to_id[aux_name][aux_value] = aux_dim
                    aux_dim += 1

        aux_to_id = new_aux_to_id

        processed_data_file = os.path.join(dst_dir, 'data.tsv')
        new_aux_cols = ['']*aux_dim
        with open(processed_data_file, 'w') as f, \
             open(data_file, 'r') as data_f:
            replicate_count = 1
            for aux_name, v in aux_to_id.items():
                if type(v) is int:
                    new_aux_cols[v] = aux_name
                else:
                    for aux_value, idx in v.items():
                        new_aux_cols[idx] = aux_name + ':' + aux_value
            print("%s\t%s\t%s" % (query_col, label_col, "\t".join(new_aux_cols)), file = f)
            reader = csv.DictReader(data_f, delimiter='\t')
            for row in reader:
                query, label = row[query_col].strip(), row[label_col].strip()
                if len(query) == 0:
                    continue
                for i in range(replicate_count):
                    aux = [0] * aux_dim
                    for aux_name, v in aux_to_id.items():
                        if type(v) is int:
                            aux[v] = row[aux_name]
                        else:
                            enum_value = row[aux_name]
                            if enum_value == '*':
                                enum_value = random.choice(list(aux_to_id[aux_name]))
                            aux[aux_to_id[aux_name][enum_value]] = 1
                    print("%s\t%s\t%s" % (query, label, "\t".join(map(str, aux))), file=f)
        
        vocab_dic = {}
        label_dic = {}
        with open(processed_data_file, 'r') as processed_data_f:
            reader = csv.DictReader(processed_data_f, delimiter='\t')
            featured_data = []
            for row in reader:
                query = row[query_col]
                words = query.split()
                wids = []
                for word in words:
                    if word not in vocab_dic:
                        # use 0 as unknown word
                        wid = len(vocab_dic) + 1
                        vocab_dic[word] = wid
                    wids.append(vocab_dic[word])

                aux = []
                for aux_col in new_aux_cols:
                    aux.append(row[aux_col])

                label_name = row[label_col]
                if label_name not in label_dic:
                    lid = len(label_dic)
                    label_dic[label_name] = lid

                label = label_dic[label_name]
               
                featured_data.append((query, wids, aux, label))
            
        with open(os.path.join(dst_dir, 'classes.txt'), 'w') as f:
            print(json.dumps(label_dic),file=f)

        with open(os.path.join(dst_dir, 'auxiliary.txt'), 'w') as f:
            print(json.dumps(aux_to_id), file=f)

        with open(os.path.join(dst_dir, 'data'), 'w') as f:
            config = {"auxiliary_dim":len(new_aux_cols), 
                      "classes":len(label_dic),  
                      "vocab_size":len(vocab_dic) + 1}
            print(json.dumps(config), file=f)
            for i in featured_data:
                print("", file=f)
                print("# %s" % i[0], file=f)
                print("words: %s" % " ".join(map(str, i[1])), file=f)
                print("aux: %s" % " ".join(["%d,%s" % (idx, v) for idx,v in enumerate(i[2])]), file=f)
                print("label: %d" % i[3], file=f)
        
        with open(os.path.join(dst_dir, 'vocab'), 'w') as f:
            for k, v in sorted(vocab_dic.items(), key=lambda x:x[1]):
                print("\t".join([k, str(v)]), file=f)
    
    def Train(self, train_file, work_dir,
              query_col = "query",
              label_col = "intent",
              aux_cols = [],
              iteration = 20, max_token = 60, batch_size = 10,
              embedding_dim = 128, filter_sizes = [3, 4, 5],
              channel = 128, verbose = False):
        cnn = CNN()
        featured_data_dir = os.path.join(work_dir, "data")
        model_dir = os.path.join(work_dir, 'model')
        if not os.path.exists(featured_data_dir):
            os.makedirs(featured_data_dir)
        self._FitData(train_file, featured_data_dir,
                             query_col, label_col, aux_cols)
        model_file = os.path.join(model_dir, "model.ckpt")
        cnn.Train(os.path.join(featured_data_dir, "data"), 
                 model_file,
                 iteration,
                 max_token,
                 batch_size,
                 embedding_dim,
                 filter_sizes,
                 channel,
                 verbose)
        copyfile(os.path.join(featured_data_dir, 'vocab'),
                 os.path.join(model_dir, 'vocab'))
        copyfile(os.path.join(featured_data_dir, 'classes.txt'),
                 os.path.join(model_dir, 'classes.txt'))
        copyfile(os.path.join(featured_data_dir, 'auxiliary.txt'),
                 os.path.join(model_dir, 'auxiliary.txt'))
        return model_dir

    def Load(self, model_file):
        self.cnn = CNN()
        self.cnn.Load(model_file)
        with open(os.path.join(os.path.dirname(model_file), 'auxiliary.txt')) as f:
            self.aux_to_id = json.loads(f.read())
        self.aux_dim = -1
        for k, v in self.aux_to_id.items():
            if type(v) is int:
                self.aux_dim = v if v > self.aux_dim else self.aux_dim
            else:
                for i,j in v.items():
                    self.aux_dim = j if j > self.aux_dim else self.aux_dim
        self.aux_dim += 1
        label_dic_file = os.path.join(os.path.dirname(model_file), 'classes.txt')
        with open(label_dic_file, 'r') as f:
            label_dic = json.loads(f.read())
            self.id_to_label = {v: k for k, v in label_dic.items()}
        vocab_file = os.path.join(os.path.dirname(model_file), 'vocab')
        with open(vocab_file, 'r') as f:
            self.word_to_id = {}
            for line in f:
                fields = line.rstrip().split('\t')
                if len(fields) != 2:
                    continue
                word, wid = fields[0], int(fields[1])
                self.word_to_id[word] = wid

    def Predict(self, query, aux = {}):
        tokenized_query = query.split()
        wids = []
        for word in tokenized_query:
            if word in self.word_to_id:
                wids.append(self.word_to_id[word])
            else:
                wids.append(0)

        aux_vec = [0] * self.aux_dim
        for aux_name, v in aux.items():
            if aux_name.endswith(':enum'):
                enum_value = v.strip()
                if enum_value == '*':
                    enum_value = random.choice(list(self.aux_to_id[aux_name]))
                aux_vec[self.aux_to_id[aux_name][enum_value]] = 1
            else:
                aux_vec[self.aux_to_id[aux_name]] = float(v)
        label_ids, probs = self.cnn.Predict([wids], [[(i,v) for i,v in enumerate(aux_vec)]])
        return (self.id_to_label[label_ids[0]], probs[0][label_ids[0]])

    def Test(self, test_file,
              query_col = "query",
              label_col = "intent",
              aux_cols = []):
        
        tp, total = 0, 0
        with open(test_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                query = row[query_col].strip()
                if len(query) == 0:
                    continue
                words = query.split()
                auxs = dict((i, row[i]) for i in aux_cols)
                true_label = row[label_col]
                predict_label,_ = self.Predict(query, auxs)
                if true_label == predict_label:
                    tp += 1
                total += 1

        return (tp, total)
