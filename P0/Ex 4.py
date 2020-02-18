from Seq0 import *

FOLDER = "../Session-04/"
filename = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]

list_genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
base = ["A", "C", "T", "G"]

print("-----| Exercise 4 |------")

for element in filename:
    seq = seq_read_fasta(FOLDER + element)
    print("Gene", element)
    print(seq_count_base(seq, base))
    #for gene in list_genes:
     #   print(gene)
      #  for letter in bases:
       #     count = seq_count_base(seq, bases)

