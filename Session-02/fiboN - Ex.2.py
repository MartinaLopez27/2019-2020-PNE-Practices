# Fibonacci - Exercise 2

def fibon(num):
    if num < 0:
        print("The first Fibonacci number is 0")
    elif num == 1:
        return 0
    elif num == 2:
        return 1
    else:
        return fibon(num - 1) + fibon(num - 2)

print("5th Fibonacci term: ", fibon(5))
print("10th Fibonacci term: ", fibon(10))
print("15th Fibonacci term: ", fibon(15))
