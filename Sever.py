import socket 

IP = socket.gethostbyname(socket.gethostname())
Port = 1233
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024

def main():
    print("[STARTING] Sever is starting.")
    sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sever.bind(add)
    sever.listen()
    print("[LISTENING] Sever is listening.")

    while True:
        conn, addr = sever.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        filename = conn.recv(SIZE).decode(FORMAT)
        #print(filename)
        print("[RECV] Filename received")
        file = open(f"data/{filename}", "wb")
        conn.send("Filename received".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        data = bytes(data, encoding='utf-8')
        print("[RECV] Filename received")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        file.close()
        conn.close()

        print(f"[Disconnected] {addr} disconnected." )



if __name__ == '__main__':
    main()