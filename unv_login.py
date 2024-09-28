import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df

def login_to_nvr(ip, username, password):
    device_info_url = f"http://{ip}:81/LAPI/V1.0/System/DeviceInfo"  # Using port 81 for device info
    
    try:
        # Attempt to access device info with Basic Auth
        device_info_response = requests.get(device_info_url, auth=HTTPBasicAuth(username, password))
        if device_info_response.status_code == 200:
            device_info = device_info_response.json()
            # Check if ResponseString indicates success
            if device_info.get('Response', {}).get('ResponseString') == "Succeed":
                return True  # Successfully fetched device info
            else:
                return False  # Device info indicates not working
        else:
            return False  # Device info request failed
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {ip}: {e}")
        return False

def update_excel(file_path, df):
    df.to_excel(file_path, index=False)

def main():
    file_path = 'nvr_credentials.xlsx'  # Path to your Excel file
    df = read_excel(file_path)
    
    # Assuming your Excel file has columns: 'IP', 'Username', 'Password', 'Status'
    for index, row in df.iterrows():
        ip = row['IP']
        username = row['Username']
        password = row['Password']
        
        if login_to_nvr(ip, username, password):
            status = 'Working'
            df.at[index, 'Status'] = status
        else:
            status = 'Not Working'
            df.at[index, 'Status'] = status
        
        # Print the status
        print(f"IP: {ip}\nStatus: {status}\n")
    
    update_excel(file_path, df)
    print("Excel file updated with login status.")

if __name__ == "__main__":
    main()
