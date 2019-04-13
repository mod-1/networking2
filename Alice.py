from socket import *
import sys


class UDPClient:

    def start(self, unreliNetPort):
        servername = 'localhost'
        serverport = unreliNetPort
        clientsocket = socket(AF_INET, SOCK_DGRAM)
        message = input('Input message: ')
        clientsocket.sendto(message.encode(), (servername, serverport))
        modifiedMessage, addr = clientsocket.recvfrom(2048)
        print(modifiedMessage.decode())
        clientsocket.close()


if __name__ == '__main__':
    myclient = UDPClient()
    myclient.start(int(sys.argv[1]))
