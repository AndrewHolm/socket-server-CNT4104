from socket import *
import sys

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare the server socket
serverPort = 8080  # Choose an appropriate port
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive...')

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1][1:]  # Fix the filename extraction

        with open(filename, 'r') as file:
            outputdata = file.read()

        # Send one HTTP header line into the socket
        response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response_header.encode())

        # Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())

        # Close client socket
        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        not_found_message = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
        connectionSocket.send((response_header + not_found_message).encode())

        # Close client socket
        connectionSocket.close()

# Close the server socket (this line will not be reached)
serverSocket.close()
sys.exit()
