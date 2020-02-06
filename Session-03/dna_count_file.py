# Opens the dna.txt file and calculates the total number of bases, and the number of the different bases

counter_A = 0
counter_C = 0
counter_T = 0
counter_G = 0
counter = 0

with open('dna.txt', 'r') as f:
    f = f.strip
    for line in f:
        for character in line:
            counter = counter + 1
            if character == "A":
                counter_A += 1
            elif character == "C":
                counter_C += 1
            elif character == "T":
                counter_T += 1
            elif character == "G":
                counter_G += 1

    f.close()

print("Total number of bases: ", counter)
print("Number of the different bases: ")
print("A: ", counter_A)
print("C: ", counter_C)
print("T: ", counter_T)
print("G: ", counter_G)
