import termcolor

class Seq:

    def __init__(self, strbases):
        bases = ['A', 'C', 'G', 'T']

        for base in strbases:
            if base not in bases:
                print("ERROR!!")
                self.strbases = "ERROR"
                return

        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

def print_seqs(seqs):
    for seq in seqs:
        print(f"Sequence {seqs.index(seq)}: (Length: {seq.len()}) {seq}")


def generate_seqs(pattern, number):
    sequence = []
    for index in range(1, number + 1):
        sequence.append(Seq(pattern * index))

    return sequence


def print_seqs(seqs, color):
    for seq in seqs:
        termcolor.cprint(f"Sequence {seqs.index(seq)}: (Length: {seq.len()}) {seq}", color)


#Main program
seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

termcolor.cprint("List 1:", "cyan")
print_seqs(seq_list1, "cyan")

termcolor.cprint("List 2:", "green")
print_seqs(seq_list2, "green")
