import socket
import json
import time
import random

from shared import delayRandomTime


def process_client_message(data, mode):
    message = json.loads(data.decode())
    seq = message['seq']
    ack = message['ack']
    length = message['length']

    new_seq = ack  # New SEQ is the received ACK
    new_ack = seq + length  # New ACK is the received SEQ plus length
    return json.dumps({'seq': new_seq, 'ack': new_ack, 'length': length}).encode()
def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    timeout = 4  # seconds

    seq = 1
    ack = 1
    length = 10  # Example length
    mode = 'auto'

    try:
        message = json.dumps({'seq': seq, 'ack': ack, 'length': length}).encode()
        delayRandomTime()
        client_socket.sendto(message, (server_address, server_port))
        print(f'Client sent {message} to server')
        while True:
            try:
                client_socket.settimeout(timeout)
                data, server = client_socket.recvfrom(4096)
                print(f"Received: {data.decode()}")
                message = process_client_message(data = data, mode = mode)
            except socket.timeout:
                print(f"Timeout, resending: {message.decode()}")
                delayRandomTime()
                client_socket.sendto(message, (server_address, server_port))
                print(f'Client sent {message} to server')

    finally:
        client_socket.settimeout(None)
        client_socket.close()


udp_client()
