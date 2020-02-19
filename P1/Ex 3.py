from Seq1 import Seq

Exercise = 3
print(f"------| Exercise {Exercise} |------")

# -- Creating a Null sequence
s1 = Seq()
# -- Creating a valid sequence
s2 = Seq("ACTGA")
# -- Create an invalid sequence
s3 = Seq("Invalid sequence")

print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")
print(f"Sequence 2: {s3}")
