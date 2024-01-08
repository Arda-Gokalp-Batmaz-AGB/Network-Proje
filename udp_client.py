import socket
import json
from colorama import init as colorama_init, Fore, Style
import random
import time

colorama_init()

def delayRandomTime():
    time.sleep(random.randint(0, 4))

def process_client_auto(seq, ack, length):
    new_seq = ack
    new_ack = seq + length
    return json.dumps({'seq': new_seq, 'ack': new_ack, 'length': length}).encode()

def process_client_manual(seq, ack, length):
    new_seq = seq
    new_ack = ack
    return json.dumps({'seq': new_seq, 'ack': new_ack, 'length': length}).encode()

def udp_client(mode):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    timeout = 4  # seconds

    max_num_packets = 33
    seq = 1
    ack = 1
    length = 10  # Example length
    ack_received = set()
    retries = {}

    if mode == 'manual':
        while True:
            try:
                inp = list(map(int, input("Enter seq, ack comma separated: ").split(',')))
                seq = inp[0]
                ack = inp[1]
                message = json.dumps({'seq': seq, 'ack': ack, 'length': length}).encode()
                client_socket.sendto(message, (server_address, server_port))
                print(f'{Fore.GREEN}Client sent {message} to server {Style.RESET_ALL}')

                client_socket.settimeout(timeout)
                data, server = client_socket.recvfrom(4096)
                response = json.loads(data.decode())
                print(f"{Fore.BLUE}Received: {data.decode()}")

            except socket.timeout:
                print(f"{Fore.RED}Timeout occurred. {Style.RESET_ALL}")
                user_choice = input("Do you want to retry? (yes/no): ").lower()
                if user_choice != 'yes':
                    break

            except ValueError:
                print(f"{Fore.RED}Invalid input format. {Style.RESET_ALL}")

    else:  # auto mode
        while seq <= max_num_packets:
            try:
                delayRandomTime()
                message = json.dumps({'seq': seq, 'ack': ack, 'length': length}).encode()
                client_socket.sendto(message, (server_address, server_port))
                print(f'{Fore.GREEN}Client sent {message} to server {Style.RESET_ALL}')

                client_socket.settimeout(timeout)
                data, server = client_socket.recvfrom(4096)
                response = json.loads(data.decode())
                if response['ack'] not in ack_received:
                    ack_received.add(response['ack'])
                    print(f"{Fore.BLUE}Received: {data.decode()}")
                    seq += 1
                else:
                    print(f"{Fore.YELLOW}Duplicate ACK detected for SEQ {response['seq']} {Style.RESET_ALL}")

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

            except ValueError:
                print(f"{Fore.RED}Invalid input format. Please enter the correct format (seq, ack).")

            if seq > max_num_packets:
                print(f"{Fore.GREEN}All packets sent. Closing connection.")
                break

    client_socket.close()





if __name__ == "__main__":
    mode = input("Enter mode (auto/manual): ")
    udp_client(mode)
