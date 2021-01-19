import sys,socket
import time
from multiprocessing import Process


HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            p=Process(target=handle_echo, args=(addr,conn))
            p.daemon=True
            p.start()
            print("start process",p)

def handle_echo(address,connection):
    data = connection.recv(BUFFER_SIZE)
    time.sleep(0.5)
    connection.sendall(data)
    #connection.shutdown(socket.SHUT_RDWR)
    connection.close()
main()
    