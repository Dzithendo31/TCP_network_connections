import socket 

IP = socket.gethostbyname(socket.gethostname())
Port = 1233
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(add)
    #now the connection has been established

    while True:
        cmd = ""
        cmd = input("enter command to send to server:\n'D' download\n'u' Upload\n'q' Query files\n")

        #command, file_name = cmd.split()
        if cmd == "u":
            
            file_name = input("Enter file_name:")
            state = input("closed 'C' or open 'O':")
            if state == "O" or state == "o":
                client.send(f"upload/{file_name}/O".encode(FORMAT))
            if state == "C" or state == "c":
                pin = input("Enter code to Lock file:")
                client.send(f"upload/{file_name}/C@{pin}".encode(FORMAT))
            upload(client,file_name)
        elif cmd == "q":
            #client.send("query/none/o@000".encode(FORMAT))
            #the program will then recieve a long string of all the Files
            client.send("query/none/o@000".encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SEVER]:\n{msg}")
        elif cmd == "d":
            filename = input('Enter filename: ')
            pin = input('Enter File key, 0 if none: ')
            client.send(f"download/{filename}/{pin}".encode(FORMAT))
            
            
            #msg = client.recv(SIZE).decode(FORMAT)
            #this will either be Sending or NOT Found
            #but before it downloads it has to check

            #then if sending
            download(filename,client)

        else:
            client.close()
            break


def upload(client,file_name):
    file = open(file_name, "rb")
    byte = file.read()
    data = byte.decode("utf-8") 
    


    #client.send("learn.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {msg}")

    client.send(data.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SEVER]: {msg}")

    file.close()
def download(file_name,client):

    # Receive the file contents from the server
    file_contents = client.recv(1024)

    # Write the file contents to a new file
    with open(file_name, 'wb') as f:
        f.write(file_contents)

    print(f'Received {file_name} from server.')
    # Close the client socket

if __name__ == '__main__':
    main()
