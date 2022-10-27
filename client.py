import socket

SIZE = 1024
PORT   = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
IP = "192.168.1.4"
ADDR = (IP , PORT)

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT) # Encode the string
    #msg_length = len(message)
    #send_length = str(msg_length).encode(FORMAT)
    #send_length += b' ' * (SIZE - len(send_length))
    #client.send(send_length)
    client.sendall(message)
    print(client.recv(2048).decode(FORMAT))

send("21;0;11;28;0;22;4;0;")
send("21;0;11;28;0;22;4;0;;;;")

send(DISCONNECT_MESSAGE)





