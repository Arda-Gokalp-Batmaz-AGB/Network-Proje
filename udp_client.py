import socket
import random
from colorama import init as colorama_init, Fore, Style

colorama_init()

def udp_client(mode):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    timeout = 4  # seconds

    max_packets = 10  # Maximum number of packets to send in auto mode
    retry_limit = 3   # Maximum number of retries for a single packet

    def send_packet(seq, ack):
        message = f"{seq},{ack}".encode()
        client_socket.sendto(message, (server_address, server_port))
        print(f'{Fore.GREEN}Client sent {message} to server {Style.RESET_ALL}')

    if mode == 'auto':
        # Initial random seq and ack
        seq, ack = random.randint(1, 100), random.randint(1, 100)

        for _ in range(max_packets):
            retry_count = 0

            while retry_count <= retry_limit:
                send_packet(seq, ack)

                try:
                    client_socket.settimeout(timeout)
                    data, server = client_socket.recvfrom(4096)
                    response = data.decode()
                    print(f"{Fore.BLUE}Received: {response}")

                    if response.startswith("error"):
                        retry_count += 1
                        if retry_count > retry_limit:
                            print(f"{Fore.RED}Max retries reached for packet {seq}, {ack}. Moving to next packet.{Style.RESET_ALL}")
                            break
                    else:
                        # Update seq and ack for the next packet based on server's response
                        ack, seq = map(int, response.split(','))  # Note the switch of ack and seq here
                        ack += 10  # Increase ack by 10 for the next packet
                        break

                except socket.timeout:
                    print(f"{Fore.RED}Timeout occurred. Retrying...{Style.RESET_ALL}")
                    retry_count += 1

            # Prepare new random seq and ack for the next series of attempts if max retries reached
            if retry_count > retry_limit:
                seq, ack = random.randint(1, 100), random.randint(1, 100)

    elif mode == 'manual':
        while True:
            seq, ack = get_user_input()
            message = f"{seq},{ack}".encode()
            client_socket.sendto(message, (server_address, server_port))
            print(f'{Fore.GREEN}Client sent {message} to server {Style.RESET_ALL}')

            try:
                client_socket.settimeout(timeout)
                data, server = client_socket.recvfrom(4096)
                response = data.decode()
                print(f"{Fore.BLUE}Received: {response}")

                if response.startswith("error"):
                    retry = input("Error occurred. Do you want to retry? (y/n): ").strip().lower()
                    if retry != 'y':
                        break

            except socket.timeout:
                print(f"{Fore.RED}Timeout occurred. Do you want to retry? (y/n): {Style.RESET_ALL}")
                retry = input().strip().lower()
                if retry != 'y':
                    break

            except ValueError:
                print(f"{Fore.RED}Invalid input format. {Style.RESET_ALL}")
                break

    client_socket.close()

def get_user_input():
    seq = input("Enter seq number: ")
    ack = input("Enter ack number: ")
    return seq, ack

if __name__ == "__main__":
    mode = input("Enter mode (auto/manual): ")
    udp_client(mode)
