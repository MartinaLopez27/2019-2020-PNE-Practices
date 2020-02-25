import socket

Exercise = 3
print(f"------| Exercise {Exercise} |------")

# SERVER IP, PORT
PORT = 8082
IP = "212.128.253.145"

while True:
  # -- Ask the user for the message
    user = input("What are you thinking about?")

  # -- Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # -- Establish the connection to the Server
    s.connect((IP, PORT))

  # -- Send the user message
    s.send(str.encode("HELLO FROM THE CLIENT!!!"))

  # -- Close the socket
    s.close()