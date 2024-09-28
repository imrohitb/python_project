import pandas as pd
import os
import socket
from datetime import datetime
import signal
import sys

# Load the Excel file
df = pd.read_excel('ip_list.xlsx')

# Define a function to handle Ctrl+C interruption
def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Exporting checked data to Excel...')
    export_to_excel(results)
    sys.exit(0)

# Register the signal handler for interruption
signal.signal(signal.SIGINT, signal_handler)

# Define a function to export data to Excel
def export_to_excel(data):
    results_df = pd.DataFrame(data, columns=['IP', 'Port', 'Ping Result', 'Status', 'Date & Time'])
    results_df.to_excel('ip_port_status.xlsx', index=False)
    print("The IP and port status has been exported to ip_port_status.xlsx")

# Define a function to check port status
def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout of 1 second
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return "Open"
        else:
            return "Closed"
    except:
        return "Error"
    finally:
        sock.close()

# Check each IP and Port
results = []
for index, row in df.iterrows():
    ip = row['IP']
    port = row['Port']
    # Ping the IP address
    ping_result = os.system(f"ping -c 1 {ip}")
    ping_status = "Reachable" if ping_result == 0 else "Unreachable"
    # Check port status if ping is successful
    if ping_result == 0:
        port_status = check_port(ip, port)
    else:
        port_status = "Host Unreachable"
    # Append results
    results.append([ip, port, ping_status, port_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    # Print the results to the command screen
    print(f"IP: {ip}, Port: {port}, Ping: {ping_status}, Status: {port_status}")

# Export the results to Excel when the script finishes normally
export_to_excel(results)
