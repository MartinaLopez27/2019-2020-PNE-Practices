# Fibonacci - Exercise 3

def fibosum(num):
    if num < 0:
        print("The first Fibonacci number is 0")
    elif num == 1:
        return 0
    elif num == 2:
        return 1
    else:
        return fibosum(num - 1) + fibosum(num - 2)


def sum_numbers(last_num):
    sum = 0
    for i in range(1, last_num + 1):
        sum = fibosum(i) + sum
    return sum

print("Sum of the First 5 terms of the Fibonacci series:", sum_numbers(5))
print("Sum of the First 10 terms of the Fibonacci series:", sum_numbers(10))
