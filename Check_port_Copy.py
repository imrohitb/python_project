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

# Function to check the status of the port for a host
def check_port_status(ip, port):
    try:
        # Create a socket connection to the host and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the connection attempt
        sock.connect((ip, port))
        sock.close()
        return "Port: Open"
    except (socket.timeout, ConnectionRefusedError):
        return "Port: Closed"
    except socket.gaierror:
        return "Port: Hostname/IP not resolved"

# Create new columns to store the ping status and port status
df['Ping_Status'] = df['IP_Address'].apply(check_host_reachability)
df['Port_Status'] = df.apply(lambda row: check_port_status(row['IP_Address'], row['Port']), axis=1)

# Save the updated DataFrame to a new Excel file
df.to_excel('ping_port_status_results.xlsx', index=False)

print("Ping and Port status check completed. Results saved to 'ping_port_status_results.xlsx'")