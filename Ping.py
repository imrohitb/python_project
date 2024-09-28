import subprocess
import csv
import re

# Function to ping an IP address and return the result
def ping_target(ip):
    try:
        # Run the ping command
        result = subprocess.check_output(["ping", "-c", "4", ip], universal_newlines=True)
        # Extract the latency from the result using regular expressions
        latency_match = re.search(r"time=(\d+\.\d+) ms", result)
        if latency_match:
            latency = latency_match.group(1)
        else:
            latency = "N/A"
        return "Ping Success", latency
    except subprocess.CalledProcessError:
        return "Ping Failed", "N/A"

# Read the list of IP addresses from a file
with open("ip_addresses.txt", "r") as file:
    ip_addresses = file.read().splitlines()

# Create a list to store ping results
ping_results = []

# Loop through the list of IP addresses and ping each one
for ip in ip_addresses:
    status, latency = ping_target(ip)
    ping_results.append([ip, status, latency])

# Save results to a CSV file
with open("ping_results.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header
    csvwriter.writerow(["IP Address", "Status", "Latency"])
    # Write the data
    for result in ping_results:
        csvwriter.writerow(result)

print("Ping results saved to ping_results.csv")