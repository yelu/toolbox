#!/usr/bin/env python

import os,sys
import json
import shutil
import csv
import random
from .log import *
from featurizer.Featurizer import Featurizer
from featurizer.NGramFeaturizer import NGramFeaturizer
from featurizer.CFGFeaturizer import CFGFeaturizer
from featurizer.FeatureShifter import FeatureShifter
from lccrf.LCCRFPy import LCCRFPy

class SlotLCCRF:
    def __init__(self):
        self._lccrfpy = None
        self._featurizer = None
        self._tagToId = None
        self._idToTag = None

    def Load(self, modelDir):
        weightsFile = os.path.join(modelDir, "lccrf.weights.txt")
        self._lccrfpy = LCCRFPy()
        self._lccrfpy.Load(weightsFile)
        self._featurizer = Featurizer.Load(os.path.join(modelDir, 'query_featurizer.p'))
        tagFile = os.path.join(modelDir, "lccrf.tags.txt")
        with open(tagFile, 'r') as f:
            self._tagToId = eval(f.readline())
            self._idToTag = dict((v,k) for k,v in self._tagToId.items())

    def Train(self, data_file, work_dir,
              query_col = "slot_xml",
              iteration = 1, 
              learning_rate = 0.001, 
              variance = 0.001,
              cfg_grammars = []):
        
        data_dir = os.path.join(work_dir, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        model_dir = os.path.join(work_dir, 'model')
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        xs, ys = self._LoadData(data_file, query_col)
        self._featurizer = Featurizer()
        unigram = NGramFeaturizer(1)
        self._featurizer.AddFeaturizer("unigram", unigram, 'tokenizedQuery')
        bigram = NGramFeaturizer(2)
        self._featurizer.AddFeaturizer("bigram", bigram, 'tokenizedQuery')
        trigram = NGramFeaturizer(3)
        self._featurizer.AddFeaturizer("trigram", trigram, 'tokenizedQuery')
        u_n1 = FeatureShifter(1)
        self._featurizer.AddFeaturizer("1gram_n1", u_n1, 'unigram')
        u_p1 = FeatureShifter(-1)
        self._featurizer.AddFeaturizer("1gram_p1", u_p1, 'unigram')
        u_n2 = FeatureShifter(2)
        self._featurizer.AddFeaturizer("1gram_n2", u_n2, 'unigram')
        u_p2 = FeatureShifter(-2)
        self._featurizer.AddFeaturizer("1gram_p2", u_p2, 'unigram')
        u_n3 = FeatureShifter(3)
        self._featurizer.AddFeaturizer("1gram_n3", u_n3, 'unigram')
        u_p3 = FeatureShifter(-3)
        self._featurizer.AddFeaturizer("1gram_p3", u_p3, 'unigram')
        b_n1 = FeatureShifter(1)
        self._featurizer.AddFeaturizer("2gram_n1", b_n1, 'bigram')
        b_p1 = FeatureShifter(-1)
        self._featurizer.AddFeaturizer("2gram_p1", b_p1, 'bigram')
        b_n2 = FeatureShifter(2)
        self._featurizer.AddFeaturizer("2gram_n2", b_n2, 'bigram')
        b_p2 = FeatureShifter(-2)
        self._featurizer.AddFeaturizer("2gram_p2", b_p2, 'bigram')
        for i, cfg_grammar in enumerate(cfg_grammars):
            cfg = CFGFeaturizer(cfg_grammar)
            self._featurizer.AddFeaturizer("cfg%d"%i, cfg, "tokenizedQuery")

        self._tagToId = {}
        lccrfQueryBinFile = os.path.join(data_dir, 'query.featurized.bin')
        with open(lccrfQueryBinFile, 'w') as f:
            for x, y in zip(xs, ys):
                res = {}
                # save tags
                tags = y
                for idx, tag in enumerate(tags):
                    if tag not in self._tagToId:
                        self._tagToId[tag] = len(self._tagToId)
                    res[idx] = [self._tagToId[tag], [-1]]

                xFeatures = self._featurizer.FitTransform(x)
                for xFeature in xFeatures:
                    end, xFid = xFeature
                    res[end][1].append(xFid)
                print(len(tags), file = f)
                for key in sorted(res):
                    print("\t".join([str(key), 
                                     str(res[key][0]), 
                                     ','.join(str(x) for x in res[key][1])]),
                          file = f)
                print("", file = f)

        self._featurizer.Save(os.path.join(model_dir, 'query_featurizer.p'))

        ## save tags.
        with open(os.path.join(model_dir, 'lccrf.tags.txt'), 'w') as f:
            print(self._tagToId, file = f)
        self._idToTag = dict((v,k) for k,v in self._tagToId.items())
        log.debug("tags saved.")

        self._lccrfpy = LCCRFPy()
        self._lccrfpy.Fit(lccrfQueryBinFile, iteration, learning_rate, variance)
        weightsFile = os.path.join(model_dir, "lccrf.weights.txt")
        self._lccrfpy.Save(weightsFile)
        log.debug("weights saved.")

    def _LoadData(self, data_file, query_col):
        import re
        xs = []
        ys = []
        with open(data_file, 'r', encoding = 'utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                query = row[query_col].strip()
                query = query.replace("<", " <")
                query = query.replace(">", "> ")
                words = []
                for token in query.split():
                    if len(token) != 0:
                        words.append(token)
                x = []
                y = []
                tag = 'o'
                #has_tag = False
                for word in words:
                    if word.startswith('<') and not word.startswith('</'):
                        tag = word[1:-1]
                        #has_tag = True
                        continue
                    if word.startswith('</'):
                        tag = 'o'
                        continue
                    x.append(word)
                    y.append(tag)
                #if has_tag:
                if len(x) != 0:
                    xs.append(x)
                    ys.append(y)
            docs = list(zip(xs, ys))
            random.shuffle(docs)
            xs, ys = tuple(zip(*docs))
        return xs, ys

    def Predict(self, query):
        res = []
        tokenizedQuery = query.strip().split()
        if len(tokenizedQuery) == 0:
            return res
        labels = self._Predict(tokenizedQuery)
        last_label = 'o'
        cur_words = []
        for cur_label, cur_word in zip(labels, tokenizedQuery):
            if cur_label != 'o':
                if cur_label != last_label:
                    if last_label != 'o':
                        res.append((last_label, " ".join(cur_words)))
                        cur_words = []
                cur_words.append(cur_word)
            elif cur_label == 'o':
                if last_label == 'o':
                    pass
                else:
                    res.append((last_label, " ".join(cur_words)))
                    cur_words = []
            last_label = cur_label
        if len(cur_words) != 0:
            res.append((last_label, " ".join(cur_words)))
        return res

    def _Predict(self, tokenizedQuery):
        xFeatures = self._featurizer.Transform(tokenizedQuery)
        x = []
        for item in xFeatures:
            x.append((item[1], item[0]))
        xLen = len(tokenizedQuery)
        y = self._lccrfpy.Predict(x, xLen)
        tags = [self._idToTag[id] for id in y]
        return tags

    def Test(self, test_data, query_col = 'slot_xml'):
        xs, ys = self._LoadData(test_data, query_col)
        predictedTags = []
        for i, x in enumerate(xs):
            y = self._Predict(x)
            predictedTags.append(y)
        stat = {}
        totalTags = 0
        rightTag = 0
        xys = zip(xs, ys)
        for i, xy in enumerate(xys):
            x, y = xy[0], xy[1]
            for j, word in enumerate(x):
                totalTags += 1
                expectedTag = y[j]
                predictedTag = predictedTags[i][j]
                if expectedTag not in stat:
                    stat[expectedTag] = {"tp":0,"fp":0,"fn":0,"tn":0}
                if predictedTag not in stat:
                    stat[predictedTag] = {"tp":0,"fp":0,"fn":0,"tn":0}
                if predictedTag == expectedTag:
                    stat[expectedTag]["tp"] += 1
                    rightTag += 1
                else:
                    stat[predictedTag]["fp"] += 1
                    stat[expectedTag]["fn"] += 1
        for key, value in stat.items():
            value["precision"] = 0.0
            if value["tp"] + value["fp"] != 0:
                value["precision"] = float(value["tp"]) / float(value["tp"] + value["fp"])
            value["recall"] = 0.0
            if value["tp"] + value["fn"] != 0:
                value["recall"] = float(value["tp"]) / float(value["tp"] + value["fn"])
            value["f1"] = 0.0
            if abs(value["precision"] + value["recall"]) > 1e-6:
                value["f1"] = 2 * value["precision"] * value["recall"] / float(value["precision"] + value["recall"])
        if rightTag == 0:
            stat["accuracy"] = 0.0
        else:
            stat["accuracy"] = float(rightTag) / float(totalTags)
        return stat
