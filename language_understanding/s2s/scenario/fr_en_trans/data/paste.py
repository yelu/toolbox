import os,sys

if __name__ == "__main__":
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    dst_file = sys.argv[3]
    with open(file1, 'r', encoding='utf-8') as f1, \
         open(file2, 'r', encoding='utf-8') as f2, \
         open(dst_file, 'w', encoding='utf-8') as df:
        
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

        print("src_seq\tdst_seq", file = df)
        for l1, l2 in zip(f1_lines, f2_lines):
            print("%s\t%s" % (l1.strip(), l2.strip()), file = df)
