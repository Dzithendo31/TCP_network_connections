import socket
import hashlib
import os

IP = socket.gethostbyname(socket.gethostname())
Port = 1222
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024
buffer = 1024



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(add)
    #now the connection has been established

    while True:
        cmd = ""
        cmd = input("enter command to send to server:\n'd' download\n'u' Upload\n'q' Query files\n")

        #command, file_name = cmd.split()
        if cmd == "u" or cmd == "U":
            
            file_name = input("Enter file_name:")
            state = input("closed 'C' or open 'O':")
            if state == "O" or state == "o":
                client.send(f"upload/{file_name}/O".encode(FORMAT))
            if state == "C" or state == "c":
                pin = input("Enter code to Lock file:")
                client.send(f"upload/{file_name}/C@{pin}".encode(FORMAT))
            upload(client,file_name)
        elif cmd == "q" or cmd == "Q":
            #client.send("query/none/o@000".encode(FORMAT))
            #the program will then recieve a long string of all the Files
            client.send("query/none/o@000".encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SEVER]:\n{msg}")
        elif cmd == "d" or cmd == "Q":
            filename = input('Enter filename: ')
            pin = input('Enter File key, 0 if none: ')
            client.send(f"download/{filename}/{pin}".encode(FORMAT))
            
            
            msg = client.recv(SIZE).decode(FORMAT)
            if msg == "NONE":
                print("File not found or Incorrect Key for File Access")
            #this will either be Sending or NOT Found
            #but before it downloads it has to check
            else:
                download(filename,client)

        else:
            "Incorrect Input, connection Lost"
            client.close()
            break


def upload(client,file_name):

    #client.send("learn.txt".encode(FORMAT))
    
    #this part waits for the message of FileName recieved
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {msg}")

    #get file size
    file_size = os.path.getsize(file_name)
    client.send(str(file_size).encode(FORMAT))
    print(file_size)
    sent = 0 #bytes


    with open(file_name, 'rb') as f:

        while sent<file_size:
            bytes_read = f.read(1096)
            client.sendall(bytes_read)
            sent += 1096
        # we use sendall to assure transimission in 
        # busy networks

    #send signal than its done
    #client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {msg}")
    #Creating and Sending A hash to check if file altered.
    file = open(file_name, "rb")
    byte = file.read()
    file_hash = hashlib.sha256(byte).hexdigest()
    client.sendall(file_hash.encode())

    ms = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {ms}")


def download(file_name,client):

    # Receive the file contents from the server
    file_contents = client.recv(1024)

    # Write the file contents to a new file
    with open(file_name, 'wb') as f:
        while file_contents:
            f.write(file_contents)
            file_contents = client.recv(1024)

    print(f'Received {file_name} from {IP}.')
    # Close the client socket

if __name__ == '__main__':
    main()
