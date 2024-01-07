import socket
import random
from colorama import init as colorama_init, Fore, Style
import time

colorama_init()

def process_server_message(data, packet_history):
    # Randomly simulate a timeout (no response)
    if random.choice([True, False]):  # 50% chance to simulate timeout
        return None

    message = data.decode()
    seq, ack = map(int, message.split(','))

    packet_key = f"{seq},{ack}"

    # Check for duplicates
    if packet_key in packet_history:
        return "error-duplicate".encode()

    # Assuming length of 10 for simplicity
    length = 10
    new_seq = ack
    new_ack = seq + length

    # Check for incorrect values
    if packet_history:
        last_seq, last_ack = packet_history[-1]
        expected_next_seq = last_ack
        expected_next_ack = last_seq + length
        if seq != expected_next_seq or ack != expected_next_ack:
            return f"error-wrong_value;expected_seq:{expected_next_seq},received_seq:{seq};expected_ack:{expected_next_ack},received_ack:{ack}".encode()

    packet_history.append((new_seq, new_ack))
    return f"{new_seq},{new_ack}".encode()

def udp_server(mode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = 'localhost'
    server_port = 12345
    server_socket.bind((server_address, server_port))
    timeout = 33  # seconds

    packet_history = []

    print(f"UDP server {mode} modunda ve {server_address} adresinde {server_port} portunda dinliyor")

    while True:
        try:
            server_socket.settimeout(timeout)
            data, address = server_socket.recvfrom(4096)
            print(f"{Fore.BLUE}Alınan veri: {data.decode()}")

            response = process_server_message(data, packet_history)
            if response:
                server_socket.sendto(response, address)
                print(f"{Fore.GREEN}Cevap gönderildi: {response.decode()}{Style.RESET_ALL}")

        except socket.timeout:
            print(f"{Fore.RED}Server zaman aşımına uğradı, geçerli bir mesaj bekliyor.{Style.RESET_ALL}")

if __name__ == "__main__":
    mode = input("Mod girin (auto/manual): ")
    udp_server(mode)
