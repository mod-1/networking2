from socket import *
import sys
import zlib


class UDPServer:

    def start(self, rcvPort):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rcvPort))
        seq_no = '0'
        while True:
            message, address = serverSocket.recvfrom(1024)
            # print('message received: ' + message.decode())
            valid, res, msg_actual = self.parse_message(message.decode(), seq_no)
            if valid:
                print(msg_actual, end='', flush=True)
                seq_no = self.compliment_seqn(seq_no)
            serverSocket.sendto(res.encode(), address)
            # print('response sent: ' + res)
        serverSocket.close()

    def parse_message(self, message, sqn):
        if message[0:2].isdigit():
            length = int(message[0:2])
            checksum = message[2:2+length]
            message_actual = message[2+length:]
            chksm = zlib.crc32(message_actual.encode())
            seq_no = message_actual[0]
            if str(chksm) == checksum and seq_no == sqn:
                res_checksum, req_chksum_len = self.gen_checksum(('ACK'+sqn).encode())
                res = req_chksum_len + res_checksum + 'ACK' + sqn
                return True, res, message_actual[1:]
        res_checksum, req_chksum_len = self.gen_checksum(('ACK' + self.compliment_seqn(sqn)).encode())
        res = req_chksum_len + res_checksum + 'ACK' + self.compliment_seqn(sqn)
        return False, res, ''

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


if __name__ == '__main__':
    myserver = UDPServer()
    myserver.start(int(sys.argv[1]))
