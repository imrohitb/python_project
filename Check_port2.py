import pandas as pd
import socket
import subprocess

# Read the Excel sheet into a DataFrame
df = pd.read_excel('Check_port.xlsx')

# Function to check the reachability of a host via ICMP (ping)
def check_host_reachability(host):
    try:
        # Use the 'ping' command to check reachability (ICMP)
        subprocess.check_call(['ping', '-c', '1', host])
        return "Ping: Reachable"
    except subprocess.CalledProcessError:
        return "Ping: Unreachable"

# Function to check the status of all ports for a host
def check_all_ports_status(ip, ports):
    port_statuses = {}
    for port in ports:
        try:
            # Create a socket connection to the host and port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Set a timeout for the connection attempt
                result = sock.connect_ex((ip, port))
                if result == 0:
                    port_statuses[f'Port_{port}'] = "Port: Open"
                else:
                    port_statuses[f'Port_{port}'] = "Port: Closed"
        except socket.timeout:
            port_statuses[f'Port_{port}'] = "Port: Timed Out"
        except ConnectionRefusedError:
            port_statuses[f'Port_{port}'] = "Port: Connection Refused"
        except socket.gaierror:
            port_statuses[f'Port_{port}'] = "Port: Hostname/IP not resolved"
        except Exception as e:
            port_statuses[f'Port_{port}'] = f"Port: Error - {str(e)}"
    return port_statuses

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    ip = row['IP_Address']
    ping_status = check_host_reachability(ip)

    if 'Ports' in row:
        ports = [int(port.strip()) for port in str(row['Ports']).split(',')]
    else:
        # If 'Ports' column is not present, you can define a default port or handle it as needed
        default_port = 80
        ports = [default_port]

    port_statuses = check_all_ports_status(ip, ports)

    # Print the results for each row
    print(f"IP Address: {ip}")
    print(f"Ping Status: {ping_status}")
    for port, status in port_statuses.items():
        print(f"{port} Status: {status}")
    print("------------------------")

print("Ping and Port status check completed.")
