import socket
import json
import time
import random
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from shared import delayRandomTime, mode

colorama_init()
def process_client_message(data, mode):
    message = json.loads(data.decode())
    seq = message['seq']
    ack = message['ack']
    length = message['length']

    new_seq = ack  # New SEQ is the received ACK
    new_ack = seq + length  # New ACK is the received SEQ plus length
    return json.dumps({'seq': new_seq, 'ack': new_ack, 'length': length}).encode()

def udp_client(mode):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    timeout = 4  # seconds

    max_num_packets = 30
    seq = 1
    ack = 1
    length = 10  # Example length
    message = json.dumps({'seq': seq, 'ack': ack, 'length': length}).encode()
    for i in range(0,max_num_packets):
        try:
            delayRandomTime()
            client_socket.sendto(message, (server_address, server_port))
            print(f'{Fore.GREEN}Client sent {message} to server {Style.RESET_ALL}')
            while True:
                try:
                    client_socket.settimeout(timeout)
                    data, server = client_socket.recvfrom(4096)
                    print(f"{Fore.BLUE}Received: {data.decode()}")
                    message = process_client_message(data = data, mode = mode)
                    break
                except socket.timeout:
                    print(f"{Fore.RED}Timeout, resending: {message.decode()}")
                    delayRandomTime()
                    client_socket.sendto(message, (server_address, server_port))
                    print(f'{Fore.GREEN}Client sent {message} to server')

        finally:
            client_socket.settimeout(None)

    client_socket.close()


udp_client(mode = mode)
