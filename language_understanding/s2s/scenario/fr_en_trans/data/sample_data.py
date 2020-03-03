from nltk import word_tokenize
import sys,random

if __name__ == "__main__":
    count = int(sys.argv[1])
    with open("europarl-v7.fr-en.en", encoding='utf-8') as en_file, \
         open("europarl-v7.fr-en.fr", encoding='utf-8') as fr_file, \
         open("en.txt", 'w', encoding='utf-8') as dst_en_file, \
         open("fr.txt", 'w', encoding='utf-8') as dst_fr_file:
        
        en_lines = en_file.readlines()
        fr_lines = fr_file.readlines()
        line_count = len(en_lines)
        random.seed(13)
        for i in range(0, count):
            rnd = random.randint(0, line_count)
            en_sent = en_lines[rnd].strip().lower()
            fr_sent = fr_lines[rnd].strip().lower()
            if len(en_sent) != 0 and len(fr_sent) != 0:
                print(" ".join(word_tokenize(en_sent)), file = dst_en_file)
                print(" ".join(word_tokenize(fr_sent)), file = dst_fr_file)
            
