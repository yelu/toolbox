from nltk.translate.bleu_score import *
import json

if __name__ == "__main__":

    hypotheses, references = [], []
    with open("./test_res.json", 'r', encoding = "utf-8") as f:  
        for i, row in enumerate(f):
            print(i)
            sample = json.loads(row)
            hypotheses.append(sample["dst_seq"].split())
            references.append([x.split() for x in sample["predicted_seqs"]])
            
    bleu = corpus_bleu(references, hypotheses)
    print(bleu)     
 
