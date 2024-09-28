import xlsxwriter
import pandas as pd
import socket
import concurrent.futures
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

# Function to check the status of a port for a host
def check_port_status(ip, port):
    try:
        # Create a socket connection to the host and port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a timeout for the connection attempt
            result = sock.connect_ex((ip, port))
            if result == 0:
                return "Port: Open"
            else:
                return "Port: Closed"
    except socket.timeout:
        return "Port: Timed Out"
    except ConnectionRefusedError:
        return "Port: Connection Refused"
    except socket.gaierror:
        return "Port: Hostname/IP not resolved"
    except Exception as e:
        return f"Port: Error - {str(e)}"

# Function to process each row in parallel
def process_row(row):
    ip = row['IP_Address']
    try:
        ping_status = check_host_reachability(ip)
        port_statuses = {}  # Dictionary to store port statuses for each port
        for port in row['Ports'].split(','):  # Assuming 'Ports' column contains comma-separated port values
            port = int(port.strip())
            try:
                port_status = check_port_status(ip, port)
            except Exception as e:
                port_status = f"Port: Error - {str(e)}"
            port_statuses[f'Port_{port}'] = port_status
    except Exception as e:
        ping_status = f"Ping: Error - {str(e)}"
        port_statuses = {'Port_Status': f"Port: Error - {str(e)}"}
    return {
        'IP_Address': ip,
        'Ping_Status': ping_status,
        **port_statuses
    }

# Use concurrent.futures.ThreadPoolExecutor with a maximum of 10 workers for parallel processing
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(process_row, df.to_dict('records')))

# Create a DataFrame from the results
result_df = pd.DataFrame(results)

# Save the updated DataFrame to a new Excel file with separate sheets for each port
with pd.ExcelWriter('ping_port_status_results.xlsx', engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='All_Status', index=False)
    for column in result_df.columns:
        if 'Port_' in column:
            port_df = result_df[['IP_Address', 'Ping_Status', column]]
            port_df.to_excel(writer, sheet_name=column, index=False)

print("Ping and Port status check completed. Results saved to 'ping_port_status_results.xlsx'")
