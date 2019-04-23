from socket import *
import sys
import zlib
import time


class UDPClient:

    def start(self, unreliNetPort, start):
        servername = 'localhost'
        serverport = unreliNetPort
        clientsocket = socket(AF_INET, SOCK_DGRAM)
        clientsocket.settimeout(0.05)
        seq_no = '0'
        message = sys.stdin.read()
        size = len(message.encode())
        i = 0
        while size > 0:
            buffer = seq_no + message[i:i+50]
            checksum, length = self.gen_checksum(buffer.encode())
            buffer = length + checksum + buffer
            clientsocket.sendto(buffer.encode(), (servername, serverport))
            print('message sent: ' + buffer)
            try:
                modifiedMessage, addr = clientsocket.recvfrom(1024)
            except timeout:
                continue
            print('response received: '.encode() + modifiedMessage)
            if self.parse_response(modifiedMessage.decode(), seq_no):
                i = i + 50
                size = size - 50
                seq_no = self.compliment_seqn(seq_no)
        clientsocket.close()
        end = time.time()
        print(end-start)

    def gen_checksum(self, bytes):
        checksum = zlib.crc32(bytes)
        length = len((str(checksum)).encode())
        if length < 10:
            length = '0' + str(length)
        else:
            length = str(length)
        return str(checksum), length

    def compliment_seqn(self, sqn):
        if sqn == '0':
            return '1'
        return '0'

    def parse_response(self, message, sqn):
        if message[0:2].isdigit():
            length = int(message[0:2])
            checksum = message[2: 2 +length]
            message_actual = message[2 + length:]
            chksm = zlib.crc32(message_actual.encode())
            seq_no = message_actual[-1]
            if str(chksm) == checksum and seq_no == sqn:
                return True
        return False


if __name__ == '__main__':
    start = time.time()
    myclient = UDPClient()
    myclient.start(int(sys.argv[1]), start)
