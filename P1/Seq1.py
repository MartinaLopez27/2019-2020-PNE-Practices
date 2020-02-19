from pathlib import Path

class Seq:
    """A class for representing sequences"""

    NULL = "NULL"  #empty
    ERROR = "ERROR"  #invalid
    VALID = "VALID"  #valid

    def __init__(self, strbases = "NULL"):

        #It is a NULL sequence (empty)?
        if strbases == self.NULL:
            self.strbases = self.NULL
            print("NULL Seq created")
            return

        # It is a invalid sequence?
        if not self.valid_str(strbases):
            self.strbases = self.ERROR
            print("INVALID Seq!")
            return

        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):
        """Method called when the object is being printed"""

        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        if self.strbases in [self.NULL, self.ERROR]:
            return 0
        else:
            return len(self.strbases)

    def valid_str(self, strbases):
        valid_bases = ['A', 'C', 'T', 'G']

        for base in strbases:
            if base not in valid_bases:
                return False

        return True

    def count_base(self, base):
        return self.strbases.count(base)

    def count(self):
        dic = {'A': self.count_base('A'), 'T': self.count_base('T'),
               'C': self.count_base('C'), 'G': self.count_base('G')}
        return dic

    def reverse(self):
        if self.strbases in [self.NULL, self.ERROR]:
            return self.strbases
        else:
            return self.strbases[::-1]

    def complement(self):
        if self.strbases in [self.NULL, self.ERROR]:
            return self.strbases

        basescom = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

        dic = ""

        for base in self.strbases:
            dic += basescom[base]

        return dic

    def read_fasta(self, filename):
        contents = Path(filename).read_text()
        body = contents.split('\n')[1:]
        self.strbases = "".join(body)
        return self
