import pandas as pd
import socket
from ping3 import ping
from openpyxl import Workbook

def check_port(ip, port):
    """Check if a port is open on a given IP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect((ip, port))
        return True
    except (socket.timeout, socket.error):
        return False
    finally:
        sock.close()

def main(input_file, output_file):
    # Read the input Excel file
    df = pd.read_excel(input_file)
    
    # Prepare a list to hold results
    results = []

    for index, row in df.iterrows():
        ip = row['IP']
        port = 5900
        
        # Ping the IP address
        ping_status = ping(ip)
        if ping_status is None:
            ping_result = 'Ping Failed'
            port_status = 'N/A'
            status = 'Not Working'
        else:
            ping_result = 'Ping Success'
            # Check if the port is open
            if check_port(ip, port):
                port_status = 'Open'
                status = 'Working'
            else:
                port_status = 'Closed'
                status = 'Not Working'

        # Print the results
        print(f"IP Address: {ip}")
        print(f"Ping Status: {ping_result}")
        print(f"Port 5900 Status: {port_status}")
        print(f"AI Status: {status}")
        print("-" * 40)

        # Append the results to the list
        results.append({
            'IP': ip,
            'Ping Status': ping_result,
            'Port 5900 Status': port_status,
            'AI Status': status
        })

    # Create a DataFrame from results
    result_df = pd.DataFrame(results)

    # Write results to an output Excel file
    result_df.to_excel(output_file, index=False)
    print(f"Results have been written to {output_file}")

if __name__ == "__main__":
    input_file = 'ai_ip.xlsx'
    output_file = 'ai_result_ip.xlsx'
    main(input_file, output_file)
