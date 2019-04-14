from socket import *
import sys
import zlib

# handle the length of checksum
class UDPClient:

    def start(self, unreliNetPort):
        servername = 'localhost'
        serverport = unreliNetPort
        clientsocket = socket(AF_INET, SOCK_DGRAM)
        for message in sys.stdin:
            size = len(message.encode())
            i = 0
            seq_no = '0'
            while size > 0:
                buffer = seq_no + message[i:i+50]
                checksum, length = self.gen_checksum(buffer.encode())
                buffer = length + checksum + buffer
                clientsocket.sendto(buffer.encode(), (servername, serverport))
                print('message sent: ' + buffer)
                modifiedMessage, addr = clientsocket.recvfrom(1024)
                print('response recieved: ' + modifiedMessage.decode())
                if self.parse_response(modifiedMessage.decode(), seq_no):
                    i = i + 50
                    size = size - 50
                    seq_no = self.compliment_seqn(seq_no)
        clientsocket.close()

    def gen_checksum(self, bytes):
        checksum = zlib.crc32(bytes)
        return str(checksum), str(len((str(checksum)).encode()))

    def compliment_seqn(self, sqn):
        if sqn == '0':
            return '1'
        return '0'

    def parse_response(self, message, sqn):
        length = int(message[0:2])
        checksum = message[2: 2 +length]
        message_actual = message[2 + length:]
        chksm = zlib.crc32(message_actual.encode())
        seq_no = message_actual[-1]
        if str(chksm) == checksum and seq_no == sqn:
            return True
        return False


if __name__ == '__main__':
    myclient = UDPClient()
    myclient.start(int(sys.argv[1]))
