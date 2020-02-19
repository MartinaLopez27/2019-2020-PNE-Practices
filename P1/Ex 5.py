from Seq1 import Seq

Exercise = 5
print(f"------| Exercise {Exercise} |------")

# -- Creating a Null sequence
s0 = Seq()
# -- Creating a valid sequence
s1 = Seq("ACTGA")
# -- Create an invalid sequence
s2 = Seq("Invalid sequence")

print(f"Sequence 0: (Length: {s1.len()}) {s0}")
print(f"A {s0.count_base()} {s0}")
print(f"Sequence 1: (Length: {s1.len()}) {s1}")
print(f"Sequence 2: (Length: {s1.len()}) {s2}")