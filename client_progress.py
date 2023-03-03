from http import client
import socket
import hashlib
import os
import ssl

IP = socket.gethostbyname(socket.gethostname())
Port = 4000
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024
buffer = 1024
#



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(add)
    #now the connection has been established

    #use of SLL to wrap the socket  with SLL
    #context = ssl.create_default_context()
    #client = context.wrap_socket(TCP_client, server_hostname="localhost")
    while True:
        cmd = ""
        cmd = input("enter command to send to server:\n'd' download\n'u' Upload\n'X' Upload\n'l' To list files\n'q' to Quit\n " )

        #command, file_name = cmd.split()
        if cmd == "u" or cmd == "U":
            
            file_name = input("Enter file_name:")
            state = input("closed 'C' or open 'O':")
            if state == "O" or state == "o":
                client.send(f"upload/{file_name}/O".encode(FORMAT))
            if state == "C" or state == "c":
                pin = input("Enter code to Lock file:")
                client.send(f"upload/{file_name}/C@{pin}".encode(FORMAT))
            else:
                print("Incorrect input.")
                continue
            try:
                #before upload changefile name if duplicate
                #so client waits for message from server of how the file is saved.
                msg = client.recv(64).decode(FORMAT)
                print(f"[SEVER]:\n{msg}")
                print("uploading")
                upload(client,file_name)

            except:
                print("Error has occured, restart App.")
                continue
        elif cmd == "l" or cmd == "L":
            #client.send("query/none/o@000".encode(FORMAT))
            #the program will then recieve a long string of all the Files
            client.send("query/none/o@000".encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SEVER]:\n{msg}")
        elif cmd == "d" or cmd == "D":
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
        elif cmd == "X" or cmd == "x":
            filename = input('Enter filename: ')
            pin = input('Enter File key, 0 if none: ')
            client.send(f"delete/{filename}/{pin}".encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            if msg == "NONE":
                print("File not found or Incorrect Key for File Delete")
            else:
                print(f"File{filename} delete")
            #wait for message and break

        
        else:
            "Incorrect Input, connection Lost"
            client.close()
            break


def upload(client,file_name):
    print("uploading now2")
    #client.send("learn.txt".encode(FORMAT))
    
    #this part waits for the message of FileName recieved

    #get file size
    file_size = os.path.getsize(file_name)
    #2A
    client.send(str(file_size).encode(FORMAT))
    print(file_size)
    sent = 0 #bytes

    print("uploading......")
    with open(file_name, 'rb') as f:

        while sent<file_size:

            bytes_read = f.read(1096)
            client.sendall(bytes_read)

            #get the hash for the specific bytes being sent
            file_hash = hashlib.sha256(bytes_read).hexdigest()
            #send the hash to the server
            client.sendall(file_hash.encode())

            #wait for the servers response on 
            msd = client.recv(SIZE).decode(FORMAT)
            if msd == "Continue":
                sent += 1096
                continue
            else:
                print("File disturedbed")
                break
        #just for message controls 
        control = client.recv(SIZE).decode(FORMAT)

def download(file_name,client):

        print("[RECV] Filename received")
        #file = open(f"data/{file_name}", "wb")
        client.send("Filename received".encode(FORMAT))

        SizeX = int(client.recv(SIZE).decode(FORMAT))
        #data = bytes(data, encoding='utf-8')
        sent = 0
        with open(f"downloads/{file_name}", 'wb') as f:
            
            while sent<SizeX:
                data = client.recv(1096)#.decode(FORMAT)
                
                computed_file_hash = hashlib.sha256(data).hexdigest()
                hash = client.recv(64).decode(FORMAT)
                if hash == computed_file_hash:
                    sent += 1096
                    f.write(data)
                    client.send("Continue".encode(FORMAT))
                else:
                    #delete file
                    os.remove(f"data/{file_name}")
                    client.send("Corrupt".encode(FORMAT))
                    break

            f.close()
        
        print("[RECV] Filename Data received")
        client.send("File data received".encode(FORMAT))


if __name__ == '__main__':
    main()
