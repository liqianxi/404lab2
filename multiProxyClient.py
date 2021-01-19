from multiprocessing import Pool
import socket
import sys

HOST = "localhost"
PORT =8001
BUFFER_SIZE = 4096
payload = "GET / HTTP/1.0\r\nHost:www.google.com\r\n\r\n"
def create_tcp_socket():
    print("Creating socket")
    try:
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        sys.exit()
    print("Successfully created socket")
    return newSocket
    
def get_remote_ip(host):
    print('Getting IP for {}'.format(host))
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.error:
        sys.exit()

    print('IP of address of {host} is {remote_ip}')
    return remote_ip


def send_data(serverSocket, payload):
    print("Sending payload")
    try:
        serverSocket.sendall(payload.encode())
    except socket.error:
        sys.exit()
    print("Send successfully")

def connect(addr):
    try:
        newSocket = create_tcp_socket()
        newSocket.connect(addr)

        send_data(newSocket, payload)
        newSocket.shutdown(socket.SHUT_WR)
        all_data = b""
        while True:
            data = newSocket.recv(4096)
            if not data:
                 break
            all_data += data
        print(all_data)
    except Exception as e:
        print(e)
    finally:
        newSocket.close()
        return
    
def main():
    my_address = [('127.0.0.1',8001)]
    with Pool() as p:
        p.map(connect,my_address*10)

main()