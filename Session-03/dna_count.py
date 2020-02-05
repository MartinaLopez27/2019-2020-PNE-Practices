#Counting DNA bases:

u_input = input("Introduce the sequence: ")

counter_A = 0
counter_C = 0
counter_T = 0
counter_G = 0

for character in u_input:
    if character == "A":
        counter_A += 1
    elif character == "C":
        counter_C += 1
    elif character == "T":
        counter_T += 1
    elif character == "G":
        counter_G += 1

print("Total length: ", len(u_input))
print("A: ", counter_A)
print("C: ", counter_C)
print("T: ", counter_T)
print("G: ", counter_G)
