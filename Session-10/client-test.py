from Client0 import Client

PORT = 8080
IP = "192.168.1.135"

for index in range(5):
    c = Client(IP, PORT)
    c.debug_talk(f"Message {index}")