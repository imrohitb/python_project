import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
from requests.exceptions import HTTPError, Timeout, RequestException
import pymysql.cursors
from datetime import datetime
import ping3

# Endpoint details
ip_database = 'localhost'
db_username = 'root'
db_password = ''
db_name = 'atm_data'

# URLs for endpoints
camera_status_endpoint = "/ISAPI/System/Video/inputs/channels"
hdd_status_endpoint = "/ISAPI/ContentMgmt/Storage"
dvr_time_endpoint = "/ISAPI/System/time"

# Timeout settings
api_timeout_seconds = 5 # Timeout in seconds for API requests
ping_timeout_seconds = 5  # Timeout in seconds for ping requests

# Function to ping the IP address using ping3 library
def ping_ip(ip_address):
    try:
        response = ping3.ping(ip_address, timeout=ping_timeout_seconds)
        return 'Working' if response is not None else 'Not Working'
    except Exception as e:
        print(f"Error pinging IP {ip_address}: {e}")
        return 'Not Working'

# Function to fetch and print camera status response for Hikvision
def fetch_camera_status(ip_address, port, username, password):
    try:
        auth = HTTPDigestAuth(username, password)
        response = requests.get(f'http://{ip_address}:{port}{camera_status_endpoint}', auth=auth, timeout=api_timeout_seconds)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        camera_statuses = {}

        for channel in root.findall('.//{http://www.hikvision.com/ver20/XMLSchema}VideoInputChannel'):
            id = channel.find('{http://www.hikvision.com/ver20/XMLSchema}id').text
            res_desc = channel.find('{http://www.hikvision.com/ver20/XMLSchema}resDesc').text.strip()

            status = 'Not Working' if 'NO VIDEO' in res_desc else 'Working'
            camera_statuses[id] = status
            print(f"Camera {id}: {status}")

        return camera_statuses
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Timeout:
        print(f'Timeout error: Request timed out after {api_timeout_seconds} seconds')
        return None
    except RequestException as req_err:
        print(f'Request error occurred: {req_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to fetch and print HDD status response
def print_hdd_status(ip_address, port, username, password):
    try:
        auth = HTTPDigestAuth(username, password)
        response = requests.get(f'http://{ip_address}:{port}{hdd_status_endpoint}', auth=auth, timeout=api_timeout_seconds)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
        status_tag = root.find('.//ns:status', namespaces=ns).text.strip().lower()

        hdd_status = 'Working' if status_tag == 'ok' else 'Not Working'
        print(f"HDD Status: {hdd_status}")
        return hdd_status
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Timeout:
        print(f'Timeout error: Request timed out after {api_timeout_seconds} seconds')
        return None
    except RequestException as req_err:
        print(f'Request error occurred: {req_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to fetch DVR time and update in the database
def fetch_and_update_dvr_time(ip_address, port, username, password):
    try:
        auth = HTTPDigestAuth(username, password)
        response = requests.get(f'http://{ip_address}:{port}{dvr_time_endpoint}', auth=auth, timeout=api_timeout_seconds)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        local_time = root.find('.//{http://www.hikvision.com/ver20/XMLSchema}localTime').text.strip()
        print("DVR Time:", local_time)

        connection = pymysql.connect(host=ip_database,
                                     user=db_username,
                                     password=db_password,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE sites_master SET DVR_Time = %s, updated_at = %s WHERE IP_Address = %s AND Port = %s"
                cursor.execute(sql, (local_time, datetime.now(), ip_address, port))
                connection.commit()
                print(f"Updated DVR Time in the database for IP: {ip_address}")
        finally:
            connection.close()
        return local_time
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Timeout:
        print(f'Timeout error: Request timed out after {api_timeout_seconds} seconds')
        return None
    except RequestException as req_err:
        print(f'Request error occurred: {req_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to update database with Login_Status, HDD_Status, Camera_Status, and Ping_Status
def update_database(ip_address, ping_status=None, login_status=None, hdd_status=None, camera_statuses=None, dvr_time=None):
    try:
        connection = pymysql.connect(host=ip_database,
                                     user=db_username,
                                     password=db_password,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            sql = """UPDATE sites_master SET Ping = %s, Login_Status = %s, HDD_Status = %s, Camera_1 = %s, Camera_2 = %s, 
                    Camera_3 = %s, Camera_4 = %s, DVR_Time = %s, updated_at = %s WHERE IP_Address = %s"""
            camera_1_status = camera_statuses.get('1', 'Not Working') if camera_statuses else None
            camera_2_status = camera_statuses.get('2', 'Not Working') if camera_statuses else None
            camera_3_status = camera_statuses.get('3', 'Not Working') if camera_statuses else None
            camera_4_status = camera_statuses.get('4', 'Not Working') if camera_statuses else None

            cursor.execute(sql, (
                ping_status, login_status, hdd_status, camera_1_status, camera_2_status, camera_3_status, camera_4_status,
                dvr_time, datetime.now(), ip_address))
            connection.commit()
            print(
                f"Updated database for IP: {ip_address} - Ping: {ping_status}, Login_Status: {login_status}, HDD_Status: {hdd_status}, Camera_1: {camera_1_status}, Camera_2: {camera_2_status}, Camera_3: {camera_3_status}, Camera_4: {camera_4_status}, DVR_Time: {dvr_time}")
    except pymysql.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as err:
        print(f'Error updating database: {err}')
    finally:
        connection.close()

# Function to fetch IP, Port, Username, and Password from sites_master table where DVR_name is 'Hikvision'
def fetch_site_details_from_database():
    try:
        connection = pymysql.connect(host=ip_database,
                                     user=db_username,
                                     password=db_password,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            sql = "SELECT IP_Address, Port, Username, Password FROM sites_master WHERE DVR_name = 'Hikvision'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.Error as e:
        print(f"Database error occurred: {e}")
        return None
    finally:
        connection.close()

# Main function to orchestrate the process
def main():
    site_details = fetch_site_details_from_database()

    if site_details:
        for site in site_details:
            ip_address = site['IP_Address']
            port = site['Port']
            username = site['Username']
            password = site['Password']

            print(f"Processing data for IP: {ip_address}")

            ping_status = ping_ip(ip_address)
            update_database(ip_address, ping_status=ping_status)

            if ping_status == 'Not Working':
                update_database(ip_address, ping_status=ping_status, login_status='Not Working')
                continue

            camera_statuses = fetch_camera_status(ip_address, port, username, password)
            hdd_status = print_hdd_status(ip_address, port, username, password)
            dvr_time = fetch_and_update_dvr_time(ip_address, port, username, password)
            update_database(ip_address, ping_status=ping_status, login_status='Working', hdd_status=hdd_status, camera_statuses=camera_statuses, dvr_time=dvr_time)
    else:
        print("No site details found for DVR_name 'Hikvision'")

if __name__ == "__main__":
    main()
