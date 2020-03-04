import socket
import termcolor
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080

FOLDER = "../Session-04/"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
EXT = ".txt"


Seq_test = [
    "ACCTCCTCTCCAG",
    "AAAAACATTAATC",
    "CAAGGTCCCCTTC",
    "CCCTAGCCTGACT",
    "AGCGCAAACGCTA",]


def get_cmd(n):
    return Seq_test[n]


def info_cmd(strseq):
    s = Seq(strseq)
    sl = s.len()
    ca = s.count_base('A')
    pa = "{:.1f}".format(100 * ca / sl)
    cc = s.count_base('C')
    pc = "{:.1f}".format(100 * cc / sl)
    cg = s.count_base('G')
    pg = "{:.1f}".format(100 * cg / sl)
    ct = s.count_base('T')
    pt = "{:.1f}".format(100 * ct / sl)

    resp = f"""Sequence: {s}
Total length: {sl}
A: {ca} ({pa}%)
C: {cc} ({pc}%)
G: {cg} ({pg}%)
T: {ct} ({pt}%)"""
    return resp


def comp_cmd(strseq):
    s = Seq(strseq)
    return s.complement()


def rev_cmd(strseq):
    s = Seq(strseq)
    return s.reverse()


def gene_cmd(name):
    s = Seq()
    s.read_fasta(FOLDER + name + EXT)
    return str(s)


# Create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()
print("SEQ Server configured!")

#Main program
while True:
    print("Waiting for clients....")

    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server Stopped!")
        ls.close()
        exit()
    else:

        req_raw = cs.recv(2000)
        req = req_raw.decode()

        lines = req.split("\n")
        line0 = lines[0].strip()

        lcmds = line0.split(' ')

        cmd = lcmds[0]

        response = ""

        if cmd == "PING":
            termcolor.cprint("PING command!", 'green')
            response = "OK!"
        elif cmd == "GET":
            termcolor.cprint("GET", 'green')
            response = get_cmd(int(arg))
        elif cmd == "INFO":
            termcolor.cprint("INFO", 'green')
            response = info_cmd(arg)
        elif cmd == "COMP":
            termcolor.cprint("COMP", 'green')
            response = comp_cmd(arg)
        elif cmd == "REV":
            termcolor.cprint("REV", 'green')
            response = rev_cmd(arg)
        elif cmd == "GENE":
            termcolor.cprint("GENE", 'green')
            response = gene_cmd(arg)
        else:
            termcolor.cprint("Unknown command!!!", 'red')
            response = "Unkwnown command"


        response += '\n'
        print(response)
        cs.send(response.encode())
        cs.close()
