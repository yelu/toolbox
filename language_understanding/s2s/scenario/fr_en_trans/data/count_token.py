import sys

def print_token_count(file_path):
    with open(file_path, encoding='utf-8') as f:
        tokens = set()
        for line in f:
            fields = line.split()
            for ele in fields:
                tokens.add(ele.strip())    
        print("%s tokens : %s" % (file_path, len(tokens)))

if __name__ == "__main__":
    
    for f in sys.argv[1:]:
        print_token_count(f)

    
