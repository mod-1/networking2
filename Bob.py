from socket import *
import sys
import zlib

# handle the length of checksum
class UDPServer:

    def start(self, rcvPort):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rcvPort))
        seq_no = '0'
        while True:
            message, address = serverSocket.recvfrom(1024)
            print('message received: ' + message.decode())
            valid, res, msg_actual = self.parse_message(message.decode(), seq_no)
            if valid:
                # print(msg_actual, end='', flush=True)
                seq_no = self.compliment_seqn(seq_no)
            serverSocket.sendto(res.encode(), address)
            print('response sent: ' + res)
        serverSocket.close()

    def parse_message(self, message, sqn):
        length = int(message[0:2])
        # print('length: ' + message[0:2])
        checksum = message[2:2+length]
        # print('checksum: ' + checksum)
        message_actual = message[2+length:]
        # print('message_actual: ' + message_actual)
        chksm = zlib.crc32(message_actual.encode())
        # print('chksm: ' + str(chksm))
        seq_no = message_actual[0]
        # print(seq_no + '   ' + sqn)
        if str(chksm) == checksum and seq_no == sqn:
            # print('valid message')
            res_checksum, req_chksum_len = self.gen_checksum(('ACK'+sqn).encode())
            res = req_chksum_len + res_checksum + 'ACK' + sqn
            return True, res, message_actual[1:]
        else:
            # print('invalid message')
            res_checksum, req_chksum_len = self.gen_checksum(('ACK' + self.compliment_seqn(sqn)).encode())
            res = req_chksum_len + res_checksum + 'ACK' + self.compliment_seqn(sqn)
            return False, res, message_actual[1:]

    def gen_checksum(self, bytes):
        checksum = zlib.crc32(bytes)
        return str(checksum), str(len((str(checksum)).encode()))

    def compliment_seqn(self, sqn):
        if sqn == '0':
            return '1'
        return '0'


if __name__ == '__main__':
    myserver = UDPServer()
    myserver.start(int(sys.argv[1]))
