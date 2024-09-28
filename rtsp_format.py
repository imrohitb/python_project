import pandas as pd

def generate_rtsp_url(ip, password):
    return f"rtsp://admin:{password}@{ip}:554/Streaming/Channels/101"

# Read IP addresses and passwords from the Excel file
data_df = pd.read_excel("data.xlsx")

# Check if the dataframe has the required columns
if 'IP' not in data_df.columns or 'Password' not in data_df.columns:
    raise ValueError("Excel file should contain 'IP' and 'Password' columns")

# Extract IP addresses and passwords from the dataframe
data = data_df[['IP', 'Password']].values.tolist()

# Generate RTSP URLs for each IP address and password
rtsp_urls = [generate_rtsp_url(ip, password) for ip, password in data]

# Print the generated RTSP URLs
for rtsp_url in rtsp_urls:
    print(rtsp_url)
