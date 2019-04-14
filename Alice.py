from socket import *
import sys


class UDPClient:

    def start(self, unreliNetPort):
        servername = 'localhost'
        serverport = unreliNetPort
        clientsocket = socket(AF_INET, SOCK_DGRAM)
        for message in sys.stdin:
            size = len(message.encode())
            i = 0
            while size > 0:
                buffer = message[i:i+64]
                clientsocket.sendto(buffer.encode(), (servername, serverport))
                i = i + 64
                size = size - 64
        modifiedMessage, addr = clientsocket.recvfrom(1024)
        print(modifiedMessage.decode())
        clientsocket.close()


if __name__ == '__main__':
    myclient = UDPClient()
    myclient.start(int(sys.argv[1]))
