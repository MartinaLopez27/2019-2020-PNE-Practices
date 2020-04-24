"""""
class Seq:
    def __init__(self, strbase):  # -- Initialize variables
        self.strbase = strbase

    def get_sequence(self):  # -- Return a variable
        return self.strbase

    def len(self):  # -- Get the lenght of a sequence
        return len(self.strbase)

    def complement(self):  # -- Change a base for its complement
        change = ''
        for letter in self.strbase:
            if letter == 'A':
                change += 'T'
            elif letter == 'T':
                change += 'A'
            elif letter == 'G':
                change += 'C'
            else:
                change += 'G'
        return Seq(change)

    def reverse(self):  # -- Get the reverse sequence
        return Seq(self.strbase[::-1])

    def count(self, base):  # -- Count how many bases are
        counter = 0
        for letter in self.strbase:
            if base == letter:
                counter += 1
        return counter

    def perc(self, base):  # -- Get the percentage
        return round((float(self.count(base)) / float(self.len())) * 100, 1)
"""""

class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def count(self, base):
        n_base = self.strbases.count(base)
        return n_base

    def perc(self, base):
        tl = len(self.strbases)
        if tl > 0:
            nbase = self.count(base)
            perc = round(100.0 * nbase / tl, 1)
        else:
            perc = 0
        return perc