from pathlib import Path

class Seq:
    """A class for representing sequences"""

    NULL = "NULL"  #empty
    ERROR = "ERROR"  #invalid

    def __init__(self, strbases = "NULL"):

        #It is a NULL sequence (empty)?
        if strbases.self == self.NULL:
            self.strbases = self.NULL
            print("NULL Seq created")
            return

        #It is a valid sequence?
        if strbases.self != self.NULL:
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
        return len(self.strbases)