import socket
import json
import random
import time
from colorama import init as colorama_init, Fore, Style

colorama_init()

# Global variables to track the last ACK and SEQ
last_ack = -1
last_seq = -1

def delayRandomTime():
    time.sleep(random.randint(0, 4))

def process_server_message(data, mode):
    global last_ack, last_seq
    message = json.loads(data.decode())
    seq = message['seq']
    ack = message['ack']
    length = message['length']

    # Check if the packet is a duplicate in manual mode
    if mode == 'manual' and seq == last_ack:
        return json.dumps({'seq': last_seq, 'ack': last_ack, 'length': length}).encode()

    # Process normally and update last ACK and SEQ
    new_seq = ack
    new_ack = seq + length
    last_ack = new_ack
    last_seq = new_seq

    return json.dumps({'seq': new_seq, 'ack': new_ack, 'length': length}).encode()

def udp_server(mode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    server_socket.bind((server_address, server_port))
    timeout = 33  # seconds

    print(f"UDP server in {mode} mode up and listening at {server_address} on port {server_port}")

    while True:
        try:
            server_socket.settimeout(timeout)
            data, address = server_socket.recvfrom(4096)
            print(f"{Fore.BLUE}Received: {data.decode()}")

            response = process_server_message(data, mode)
            if response:
                delayRandomTime()
                server_socket.sendto(response, address)
                print(f"{Fore.GREEN}Response {response.decode()} sent to {address}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Simulating lost/corrupted packet.")

        except socket.timeout:
            print(f"{Fore.RED}Server Timeout, resending: {response.decode()}")
            delayRandomTime()
            server_socket.sendto(response, address)
            print(f'{Fore.GREEN}Server sent {response} to client')

if __name__ == "__main__":
    mode = input("Enter mode (auto/manual): ")
    udp_server(mode)
