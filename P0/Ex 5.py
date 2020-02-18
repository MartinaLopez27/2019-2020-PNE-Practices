from Seq0 import *

FOLDER = "../Session-04/"
ext = ".txt"
filename = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
base = ["A", "C", "T", "G"]

print("-----| Exercise 5 |------")

for element in filename:
    seq = seq_read_fasta(FOLDER + element + ext)
    print(f"Gene {element}: {seq_count(seq)}")