import socket
import random
import json
from time import sleep
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from shared import delayRandomTime, mode

colorama_init()
def process_server_message(data, mode):
    message = json.loads(data.decode())
    seq = message['seq']
    ack = message['ack']
    length = message['length']

    # In automatic mode, randomly decide if the packet is lost/corrupted
    if mode == 'auto' and random.choice([True, False]):
        return None

    new_seq = ack  # New SEQ is the received ACK
    new_ack = seq + length  # New ACK is the received SEQ plus length
    return json.dumps({'seq': new_seq, 'ack': new_ack, 'length': length}).encode()
def udp_server(mode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    server_socket.bind((server_address, server_port))
    timeout = 15  # seconds


    print(f"UDP server in {mode} mode up and listening at {server_address} on port {server_port}")

    while True:
        server_socket.settimeout(timeout)
        data, address = server_socket.recvfrom(4096)
        print(f"{Fore.BLUE}Received: {data.decode()}")
        response = process_server_message(data, mode)
        try:
            if response:
                delayRandomTime()
                server_socket.sendto(response, address)
                print(f"{Fore.GREEN} {response} package sent to {address}")
            else:
                print(f"{Fore.RED} Simulating lost/corrupted packet.")
        except socket.timeout:
            print(f"{Fore.RED} Server Timeout, resending: {response.decode()}")
            delayRandomTime()
            server_socket.sendto(response, address)
            print(f'{Fore.GREEN} Server sent {response} to client')

udp_server(mode=mode)
