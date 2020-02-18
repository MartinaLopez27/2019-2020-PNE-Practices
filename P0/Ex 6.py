from Seq0 import *

FOLDER = "../Session-04/"
filename = "U5.txt"
gene = "U5"

print("------| Exercise 6 |------")

print("Gene", gene)
seq = seq_read_fasta(FOLDER + filename)

print("Frag: ", seq[0:20])
print("Rev: ", seq_reverse(seq[0:20]))
