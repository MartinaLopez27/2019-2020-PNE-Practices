# Opens the dna.txt file and calculates the total number of bases, and the number of the different bases

with open('dna.txt', 'r') as f:
    counter_A = 0
    counter_C = 0
    counter_T = 0
    counter_G = 0
    for line in f:
        for character in line:
            if character == "A":
                counter_A += 1
            elif character == "C":
                counter_C += 1
            elif character == "T":
                counter_T += 1
            elif character == "G":
                counter_G += 1

    final_counter = counter_A + counter_C + counter_T + counter_G
    f.close()

print("Total number of bases: ", final_counter)
print("Number of the different bases")
