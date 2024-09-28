import socket

def check_udp_port(ip, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(1)  # Set a timeout for the socket

    try:
        udp_socket.sendto(b'', (ip, port))
        data, addr = udp_socket.recvfrom(1024)
        print(f"IP address {ip} is listening on UDP port {port}")
    except socket.error:
        print(f"IP address {ip} is not listening on UDP port {port}")
    finally:
        udp_socket.close()

def check_all_ips(port):
    # Replace the IP range based on your network configuration
    for i in range(1, 255):
        ip = f'192.168.1.0 {i}'  # Modify this according to your network configuration
        check_udp_port(ip, port)

# Replace 123 with the desired UDP port number
check_all_ips(123)