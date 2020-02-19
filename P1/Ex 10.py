from Seq1 import Seq

Practice = 1
Exercise = 9

Folder = "../Session-04/"
Ext = ".txt"
GenesFile = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
Bases = ['A', 'T', 'C', 'G']

print(f"------| Practice {Practice}, Exercise {Exercise} |------")

for gene in GenesFile:
    l = Seq().read_fasta(Folder + gene + Ext)   #Make the seq "easy" to read

    dic = l.count()   #Make a disctionary that counts the values

    listl = list(dic.values())   #Make a list with those values

    m = max(listl)    #Find out the most common one

    print(f"Gene {gene}: Most frequent Base: {Bases[listl.index(m)]}")