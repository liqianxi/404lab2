import socket,sys
import time

#define address
HOST = ""
PORT = 8001

def main():
    try:
        newSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        newSocket.bind((HOST,PORT))
        newSocket.listen(2) # listen mode
    except Exception as e:
        print(e)
        sys.exit()
    else:
        while True:
            connection,address = newSocket.accept()
            print("Connection:",address)
            data = connection.recv(1024)
            time.sleep(0.4)
            connection.sendall(data)
            connection.close()
main()


