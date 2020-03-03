import random
from nltk.tokenize import WordPunctTokenizer

if __name__ == "__main__":

    src_file_path = './ChitchatData021516.txt'
    dst_file_path = './train.tsv'
    
    tokenizer = WordPunctTokenizer()
    with open(dst_file_path, 'w', encoding='utf-8', errors='ignore') as dst_file, \
         open(src_file_path, 'r', encoding='utf-8', errors='ignore') as src_file:
        
        print("src_seq\tdst_seq", file = dst_file)
        for line in src_file:
            line = line.strip()
            if len(line) == 0:
                continue
            fields = line.split('\t')
            q, a = fields[3], fields[6]
            tokenize_q = tokenizer.tokenize(q.lower().replace("\"", ""))
            tokenize_a = tokenizer.tokenize(a.lower().replace("\"", ""))
            if len(tokenize_q) == 0 or len(tokenize_a) == 0:
                continue
            print(" ".join(tokenize_q) + '\t' + " ".join(tokenize_a), file=dst_file)
