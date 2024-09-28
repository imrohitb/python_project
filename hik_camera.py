import requests
import mysql.connector
from mysql.connector import Error
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET

# Replace these variables with your actual values
ip_address = '172.55.26.230'
port = '81'
api_username = 'admin'
api_password = 'admin123'
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'atm_data'

api_url = f'http://{ip_address}:{port}/ISAPI/System/Video/inputs/channels'

# Function to get data from API using HTTP Digest Authentication
def get_api_data(url, username, password):
    response = requests.get(url, auth=HTTPDigestAuth(username, password))
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        response.raise_for_status()

# Function to parse XML data
def parse_xml_data(xml_data):
    root = ET.fromstring(xml_data)
    ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
    channels = root.findall('ns:VideoInputChannel', ns)
    
    camera_status = []
    for channel in channels:
        res_desc = channel.find('ns:resDesc', ns).text
        if res_desc == 'NO VIDEO':
            status = 'Not Working'
        else:
            status = 'Working'
        camera_status.append(status)
    
    return camera_status

# Function to insert data into MySQL
def insert_into_sites_master(camera_status, login_status):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO sites_master (Camera_1, Camera_2, Camera_3, Camera_4, Login_Status)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (*camera_status, login_status))
            connection.commit()
            print("Data inserted successfully")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main script logic
def main():
    try:
        xml_data, status_code = get_api_data(api_url, api_username, api_password)
        
        # Determine Login_Status
        if status_code == 200:
            login_status = 'Working'
        else:
            login_status = 'Not Working'

        # Parse XML data to get camera statuses
        camera_status = parse_xml_data(xml_data)

        # Insert data into sites_master
        insert_into_sites_master(camera_status, login_status)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
