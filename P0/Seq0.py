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


def seq_count_base(seq, base):
    return seq.count(base)


def seq_count(seq):
    dic = {'A': seq_count_base(seq, 'A'), 'T': seq_count_base(seq, 'T'),
           'C': seq_count_base(seq, 'C'), 'G': seq_count_base(seq, 'G')}
    return dic


def seq_reverse(seq):
    return seq[::-1]


def seq_complement(seq):
    dictionary = {'A': "T", 'T': "A", 'C': "G", 'G': "C"}
    str = ""
    for base in seq:
        str += dictionary[base]
    return str
