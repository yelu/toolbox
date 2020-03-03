import random
from nltk.tokenize import WordPunctTokenizer

''' 
    1. Read from 'movie-lines.txt'
    2. Create a dictionary with ( key = line_id, value = text )
'''
def get_id2line(dir):
    lines=open(dir + '/movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
    id2line = {}
    for line in lines:
        _line = line.split(' +++$+++ ')
        if len(_line) == 5:
            id2line[_line[0]] = _line[4]
    return id2line

'''
    1. Read from 'movie_conversations.txt'
    2. Create a list of [list of line_id's]
'''
def get_conversations(dir, ):
    conv_lines = open(dir + '/movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')
    convs = [ ]
    for line in conv_lines[:-1]:
        _line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
        convs.append(_line.split(','))
    return convs

'''
    1. Get each conversation
    2. Get each line from conversation
    3. Save each conversation to file
'''
def extract_conversations(convs,id2line,dir=''):
    idx = 0
    for conv in convs:
        f_conv = open(dir + str(idx)+'.txt', 'w')
        for line_id in conv:
            f_conv.write(id2line[line_id])
            f_conv.write('\n')
        f_conv.close()
        idx += 1

'''
    Get lists of all conversations as Questions and Answers
    1. [questions]
    2. [answers]
'''
def gather_dataset(convs, id2line):
    questions = []; answers = []

    for conv in convs:
        if len(conv) %2 != 0:
            conv = conv[:-1]
        for i in range(len(conv)):
            if i%2 == 0:
                questions.append(id2line[conv[i]])
            else:
                answers.append(id2line[conv[i]])

    return questions, answers


'''
    We need 4 files
    1. train.enc : Encoder input for training
    2. train.dec : Decoder input for training
    3. test.enc  : Encoder input for testing
    4. test.dec  : Decoder input for testing
'''
def prepare_seq2seq_files(questions, answers, dir,TESTSET_SIZE = 30000):
     
    # choose 30,000 (TESTSET_SIZE) items to put into testset
    test_ids = random.sample([i for i in range(len(questions))],TESTSET_SIZE)
    tokenizer = WordPunctTokenizer()
    with open(dir + '/train.tsv', 'w') as train_file:
        print("src_seq" + "\t" + "dst_seq", file=train_file)
        for q, a in zip(questions, answers):
            # remove double quots, it is reserved for csv format
            q, a = tokenizer.tokenize(q.lower().replace("\"", "")), tokenizer.tokenize(a.lower().replace("\"", ""))
            print(" ".join(q) + '\t' + " ".join(a), file=train_file)


if __name__ == "__main__":
    dir = "./cornell movie-dialogs corpus"
    id2line = get_id2line(dir)
    print('>> gathered id2line dictionary.\n')
    convs = get_conversations(dir)
    print('>> gathered conversations.\n')
    questions, answers = gather_dataset(convs,id2line)
    print(questions[:2])
    print('>> gathered questions and answers.\n')
    prepare_seq2seq_files(questions, answers, dir)