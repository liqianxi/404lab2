
from multiprocessing import Pool,Process
import time
import socket
import sys

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f"Getting IP for {host}")
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.error:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip
def handle_request(connection,address,proxy_end):
    data = connection.recv(BUFFER_SIZE)
    print(f"send data to google")
    proxy_end.sendall(data)
    proxy_end.shutdown(socket.SHUT_WR)
    data2 = b""
    while True:
        data = proxy_end.recv(BUFFER_SIZE)
        if not data:
                break
        data2 += data
    #print(f"sending received data {data2} to client")
    connection.send(data2)
def main():
    host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("start proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST,PORT))
        proxy_start.listen(2)
        while True:
            connection, address = proxy_start.accept()
            print("Connected by",address)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                ip = get_remote_ip(host)
                proxy_end.connect((ip,port))
                p=Process(target=handle_request, args=(connection,address,proxy_end))
                p.daemon=True
                p.start()
                print("Start process ",p)
            connection.close()
if __name__ == "__main__":
    main()



