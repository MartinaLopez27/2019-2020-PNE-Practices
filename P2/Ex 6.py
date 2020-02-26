from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

folder = "../Session-04/"
ext = ".txt"
gene = "FRAT1"

IP = "212.128.253.145"
PORT = 8080


c = Client(IP, PORT)
print(c)

file = Seq().read_fasta(folder + gene + ext)
bases = str(file)

length = 10

print(f"Gene {gene}: {bases}")
c.talk(f"Sending {gene} Gene to the server, in fragments of {length} bases...")


for index in range(5):
    frag = bases[index * length :(index + 1) * length]

    print(f"Fragment {index + 1}: {frag}")
    c.talk(f"Fragment {index + 1}: {frag}")