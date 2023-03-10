import socket 
import csv

IP = socket.gethostbyname(socket.gethostname())
Port = 1233
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024

#an Array to act as a Database :: 1. Name of File, 2. boolean Open or Locked 3. passCode ::default to 0000
class File:
    def __init__(self,name,open,pinCode):
         self.name = name
         self.open = open
         self.pinCode = pinCode
    
def main():
    my_files = []
    send_to_array(my_files)
    #this is the array for storing our File objects
    print("[STARTING] Sever is starting.")
    sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sever.bind(add)
    sever.listen()
    print("[LISTENING] Sever is listening.")

    while True:
        conn, addr = sever.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        #connection has been Established here
        while True:

            #in command the server expert like 
            #upload/file_name.txt/c@0001
            #download/file_name.txt/O

            #now lets handle this request message
            command =conn.recv(SIZE).decode(FORMAT)
            print(command)
            comnd,filename,state = command.split("/")

            #now to handle the locked part

            if comnd == "upload":
                if state[0] == "C":
                    #then the file should be closed with passCode
                    c,code = state.split("@")
                    my_files.append(File(filename,True,code))
                    save_file("data/saved.csv",filename,"True",code)
                else:
                    #this will be when the file is open
                    my_files.append(File(filename,False,0000))
                    save_file("data/saved.csv",filename,"False",0000)
                #then call the uploading stuff
                #filename = conn.recv(SIZE).decode(FORMAT)
                upload(filename,conn)
            elif comnd == "query":
                if len(my_files) == 0:
                    #if the array is empty there are no files in the server
                    conn.send("No files in server".encode(FORMAT))
                else:
                    #print them all to the client server
                    String = ""
                    String = query(my_files, String)
                    conn.send(String.encode(FORMAT))
                    #the string is sent to user
                    print("There are Files")
            elif comnd == "download":
                #this where it gonna check even the passwords and stuff
                
                download(filename,conn,addr)

            else:
                conn.close()
                print(f"[Disconnected] {addr} disconnected." )


        #print(filename)



def upload(file_name,conn):
        print("[RECV] Filename received")
        file = open(f"data/{file_name}", "wb")
        conn.send("Filename received".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        data = bytes(data, encoding='utf-8')
        print("[RECV] Filename Data received")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        file.close()

def download(file_name,client,addr):
    #this is the method to download files from this server
    #two parameterfile name and the socket connection
    try:
        with open(f"data/{file_name}", 'rb') as f:
            file_contents = f.read()
        # Send the file contents to the client
        client.sendall(file_contents)
        print(f'Sent {file_name} to {addr}.')
    except Exception as e:
        # If an error occurs, send an error message to the client
        error_message = f'Error: {str(e)}'
        client.sendall(error_message.encode('utf-8'))

def query(my_files, String):
    #will take an array parameter of the files
    String = ""
    #this will be the string sent on to the client
    for obj in my_files:
        String = String + obj.name + "  " + str(obj.pinCode) + "\n"
    return String
def save_file(CSV,file_name,ope,pin):
        with open(CSV, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([file_name,ope,pin])

def send_to_array(array):
    with open("data/saved.csv", newline = '') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')

        for row in reader:
            ins_File = File(row[0],row[1],row[2])
            print(row[0])
            array.append(ins_File)

        
if __name__ == '__main__':
    main()
