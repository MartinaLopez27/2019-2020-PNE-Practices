from Seq0 import *

FOLDER = "../Session-04/"
filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]

list_genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
bases = ["A", "C", "T", "G"]

print("-----| Exercise 4 |------")

counter = 0
for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print("Gene", list_genes[counter])
    counter += 1
    for base in bases:
        print(f"  {base}: {seq_count_base(seq, base)}")