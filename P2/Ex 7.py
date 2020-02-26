from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 7

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

folder = "../Session-04/"
ext = ".txt"
gene = "FRAT1"

IP = "192.168.1.136"
PORT = 8080


c1 = Client(IP, PORT)
c2 = Client(IP, PORT + 1)

print(c1)
print(c2)


file = Seq().read_fasta(folder + gene + ext)
bases = str(file)

length = 10

print(f"Gene {gene}: {bases}")


msg = f"Sending {gene} Gene to the server, in fragments of {length} bases..."

c1.talk(msg)
c2.talk(msg)


for index in range(10):
    frag = bases[index * length : (index + 1) * length]

    # Client's console
    print(f"Fragment {index + 1}: {frag}")

    # Send to the server
    msg_2 = f"Fragment {index + 1}: {frag}"

    if index % 2:
        c2.talk(msg_2)

    else:
        c1.talk(msg_2)