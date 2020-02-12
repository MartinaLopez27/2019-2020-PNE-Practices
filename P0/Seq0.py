from pathlib import Path

def seq_ping():
    print("OK!")


def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()
    file = file_contents.split('\n')
    body = "".join(file[1:])
    return(body)


def seq_len(seq):
    return(len(seq))

def  seq_count_base(seq, base):
    counter_A = 0
    counter_C = 0
    counter_T = 0
    counter_G = 0

    for character in seq:
        if character == "A":
            counter_A += 1
        elif character == "C":
            counter_C += 1
        elif character == "T":
            counter_T += 1
        elif character == "G":
            counter_G += 1

    print("A: ", counter_A)
    print("C: ", counter_C)
    print("T: ", counter_T)
    print("G: ", counter_G)
