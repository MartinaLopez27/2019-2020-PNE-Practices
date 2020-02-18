from Seq0 import *

FOLDER = "../Session-04/"
filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
base = ["A", "C", "T", "G"]

print("-----| Exercise 5 |------")

for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print(f"Gene {element}: {seq_count(seq)}")