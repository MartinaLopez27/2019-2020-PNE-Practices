from Seq1 import Seq

Practice = 1
Exercise = 9

Folder = "../Session-04/"
GenesFile = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
Ext = ".txt"

print(f"------| Practice {Practice}, Exercise {Exercise} |------")

# -- Create a Null sequence
l = Seq()

# -- Initialize the null seq with the given file in fasta format
l.read_fasta(Folder + GenesFile[0] + Ext)

print(f"Sequence: (Length: {l.len()}) {l}")
print(f"Bases: {l.count()}")
print(f"Rev: {l.reverse()}")
print(f"Comp: {l.complement()}")