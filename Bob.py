from socket import *
import sys


class UDPServer:

    def start(self, rcvPort):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rcvPort))
        while True:
            buffer = bytearray()
            message, address = serverSocket.recvfrom(1024)
            while message[-1] != ord('\n'):
                buffer = buffer + message
                message, address = serverSocket.recvfrom(1024)
            buffer = buffer + message
            print(buffer.decode(), end='', flush=True)
            serverSocket.sendto('success'.encode(), address)
        serverSocket.close()


if __name__ == '__main__':
    myserver = UDPServer()
    myserver.start(int(sys.argv[1]))
