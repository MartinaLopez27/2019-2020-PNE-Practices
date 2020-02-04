# Fibonacci - Exercise 1

def Fibonacci(num):
    if num < 0:
        print("The first Fibonacci number is 0")
    elif num == 1:
        return 0
    elif num == 2:
        return 1
    else:
        return Fibonacci(num - 1) + Fibonacci(num - 2)

print(Fibonacci(11))