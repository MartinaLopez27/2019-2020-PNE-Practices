from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

folder = "../Session-04/"
ext = ".txt"
gene = "U5"

IP = "192.168.1.136"
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)

# -- Print it
print(c)


file = Seq().read_fasta(folder + gene + ext)

c.debug_talk(f"Sending {gene} Gene to the server...")
c.debug_talk(str(file))
