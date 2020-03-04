from Client0 import Client

PRACTICE = 3
EXERCISE = 7

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "127.0.0.1"
PORT = 8080

c = Client(IP, PORT)
print(c)


print("* Testing PING...")
print(c.talk("PING"))


print("* Testing GET...")
for index in range(5):
    cmd = f"GET {index}"
    print(f"{cmd}: {c.talk(cmd)}", end="")


print()
print("* Testing INFO...")
seq = c.talk("GET 0")
cmd = f"INFO {seq}"
print(c.talk(cmd))


print()
print("* Testing COMP...")
cmd = f"COMP {seq}"
print(cmd, end="")
print(c.talk(cmd))


print()
print("* Testing REV...")
cmd = f"REV {seq}"
print(cmd, end="")
print(c.talk(cmd))


print()
print("* Testing GENE...")
for gene in ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]:
    cmd = f"GENE {gene}"
    print(cmd)
    print(c.talk(cmd))