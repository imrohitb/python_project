import subprocess
import pygetwindow as gw
import time

def change_dns_server(primary_dns, secondary_dns):
    try:
        # Open Network Settings
        subprocess.run(["control.exe", "ncpa.cpl"])
        time.sleep(1)  # Allow time for the Network Connections window to open

        # Find the Network Connections window
        connections_window = gw.getWindowsWithTitle("Network Connections")[0]

        # Activate the window
        connections_window.activate()

        # Send keystrokes to open properties (Alt + Enter)
        gw.typewrite(["alt", "enter"])
        time.sleep(1)  # Allow time for the Properties window to open

        # Find the Properties window
        properties_window = gw.getWindowsWithTitle("Properties")[0]

        # Activate the window
        properties_window.activate()

        # Send keystrokes to navigate to TCP/IPv4 properties (Alt + T)
        gw.typewrite(["alt", "t"])
        time.sleep(1)  # Allow time for the TCP/IPv4 Properties window to open

        # Find the TCP/IPv4 Properties window
        ipv4_properties_window = gw.getWindowsWithTitle("Internet Protocol Version 4 (TCP/IPv4) Properties")[0]

        # Activate the window
        ipv4_properties_window.activate()

        # Send keystrokes to navigate to DNS settings (Alt + A)
        gw.typewrite(["alt", "a"])
        time.sleep(1)  # Allow time for the DNS Servers window to open

        # Find the DNS Servers window
        dns_servers_window = gw.getWindowsWithTitle("DNS Servers")[0]

        # Activate the window
        dns_servers_window.activate()

        # Send keystrokes to input primary DNS and secondary DNS
        gw.typewrite(primary_dns)
        gw.typewrite(["tab"])
        gw.typewrite(secondary_dns)

        # Save the changes (Alt + S)
        gw.typewrite(["alt", "s"])

        print("DNS server changed successfully.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Specify the desired DNS servers
    primary_dns_server = "8.8.8.8"
    secondary_dns_server = "8.8.4.4"

    # Call the function to change DNS server
    change_dns_server(primary_dns_server, secondary_dns_server)
