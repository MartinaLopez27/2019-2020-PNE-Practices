from Seq1 import Seq

Practice = 1
Exercise = 6
print(f"------| Practice {Practice}, Exercise {Exercise} |------")

# -- Creating a Null sequence
s0 = Seq()
# -- Creating a valid sequence
s1 = Seq("ACTGA")
# -- Create an invalid sequence
s2 = Seq("Invalid sequence")

for num, l in enumerate([s0, s1, s2]):
    print(f"Sequence {num}: (Length: {l.len()}) {l}")
    print(f" Bases: {l.count()}")
