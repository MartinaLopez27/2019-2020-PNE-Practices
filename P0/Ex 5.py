from Seq0 import *

FOLDER = "../Session-04/"
filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
base = ["A", "C", "T", "G"]

print("-----| Exercise 5 |------")

d = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print(d['A'], d['T'], d['C'], d['G'])
    seq_count(seq)