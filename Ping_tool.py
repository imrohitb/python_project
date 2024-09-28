import subprocess
import re
import datetime

def ping_ip(ip_address):
    try:
        output = subprocess.check_output(['ping', '-c', '4', ip_address]).decode('utf-8')
        return output
    except subprocess.CalledProcessError:
        return None

def parse_ping_report(output):
    if output:
        latency_pattern = r"min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+"
        match = re.search(latency_pattern, output)
        if match:
            latency = match.group(1)
        else:
            latency = "Unknown"

        ping_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "ping_report": "Success",
            "latency": latency,
            "ping_date_time": ping_date_time
        }
    else:
        return {
            "ping_report": "Failed",
            "latency": "Unknown",
            "ping_date_time": "Unknown"
        }

def main():
    ip_address = input("Enter IP address to ping: ")
    output = ping_ip(ip_address)
    result = parse_ping_report(output)
    print("Ping Report:", result["ping_report"])
    print("Latency:", result["latency"])
    print("Ping Date & Time:", result["ping_date_time"])

if __name__ == "__main__":
    main()
