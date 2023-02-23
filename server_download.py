import socket

# Define server host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)

print('Server started!')

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    print(f'Client {client_address} connected.')

    # Receive the filename from the client
    filename = client_socket.recv(1024).decode('utf-8')

    try:
        # Open the file and read its contents
        with open(filename, 'rb') as f:
            file_contents = f.read()

        # Send the file contents to the client
        client_socket.sendall(file_contents)
        print(f'Sent {filename} to {client_address}.')
    except Exception as e:
        # If an error occurs, send an error message to the client
        error_message = f'Error: {str(e)}'
        client_socket.sendall(error_message.encode('utf-8'))

    # Close the client socket
    client_socket.close()
