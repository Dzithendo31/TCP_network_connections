import socket

# Define server host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Get the filename from the user
filename = input('Enter filename: ')

# Send the filename to the server
client_socket.sendall(filename.encode('utf-8'))

# Receive the file contents from the server
file_contents = client_socket.recv(1024)

# Write the file contents to a new file
with open(filename, 'wb') as f:
    f.write(file_contents)

print(f'Received {filename} from {SERVER_HOST}.')
# Close the client socket
client_socket.close()
