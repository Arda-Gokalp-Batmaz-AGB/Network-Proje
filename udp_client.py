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
    ack_received = set()  # Track received acknowledgments
    retries = {}  # Track retries for each packet
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
                    response = json.loads(data.decode())
                    if response['ack'] in ack_received:
                        print(f"{Fore.YELLOW}Duplicate ACK detected for SEQ {response['seq']} {Style.RESET_ALL}")
                    else:
                        ack_received.add(response['ack'])
                        print(f"{Fore.BLUE}Received: {data.decode()}")
                        message = process_client_message(data = data, mode = mode)
                        break
                except socket.timeout:
                    print(f"{Fore.RED}Timeout, resending: {message.decode()}")
                    seq = json.loads(message.decode())['seq']
                    if seq in retries:
                        retries[seq] += 1
                    else:
                        retries[seq] = 0
                    delayRandomTime()
                    client_socket.sendto(message, (server_address, server_port))
                    print(f'{Fore.GREEN}Client sent {message} to server')

        finally:
            client_socket.settimeout(None)
        if seq in retries and retries[seq] >= 10:
            print(f"{Fore.RED}Packet {seq} is assumed lost after 3 attempts. {Style.RESET_ALL}")
    client_socket.close()


udp_client(mode = mode)
