from Seq1 import Seq

Practice = 1
Exercise = 4
print(f"------| Practice {Practice}, Exercise {Exercise} |------")

# -- Creating a Null sequence
s1 = Seq()
# -- Creating a valid sequence
s2 = Seq("ACTGA")
# -- Create an invalid sequence
s3 = Seq("Invalid sequence")

print(f"Sequence 1: (Length: {s1.len()}) {s1}")
print(f"Sequence 1: (Length: {s2.len()}) {s2}")
print(f"Sequence 1: (Length: {s3.len()}) {s3}")