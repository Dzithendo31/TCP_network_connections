import socket 

IP = socket.gethostbyname(socket.gethostname())
Port = 1233
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(add)


    file = open("learn.txt", "rb")
    byte = file.read()
    data = byte.decode("utf-8") 
    
    print(data)

    client.send("learn.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {msg}")

    client.send(data.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {msg}")

    file.close()
    client.close()

if __name__ == '__main__':
    main()