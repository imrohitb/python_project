import requests
from requests.auth import HTTPDigestAuth
import mysql.connector
from mysql.connector import Error
import json
import subprocess

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'atm_data'
}

# Function to ping an IP address with timeout
def ping_ip(ip_address, timeout=10):
    try:
        # Ping command for Windows
        command = ["ping", "-n", "1", "-w", str(timeout * 1000), ip_address]

        # Run the ping command with timeout
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

        # Check the return code
        if response.returncode == 0:
            return True
        else:
            return False

    except subprocess.TimeoutExpired:
        print(f"Ping timed out for IP address {ip_address}")
        return False
    except Exception as e:
        print(f"Error pinging IP address {ip_address}: {e}")
        return False

# Function to update Login_Status and Ping in the database
def update_login_ping_status(cursor, conn, ip_address, login_status, ping_status):
    try:
        # Prepare SQL query to update the Login_Status and Ping columns
        sql = "UPDATE sites_master SET Login_Status = %s, Ping = %s, updated_at = NOW() WHERE ip_address = %s"
        val = (login_status, ping_status, ip_address)

        # Debugging: Print the SQL query and values
        print(f"Executing SQL: {sql} with values {val}")

        # Execute SQL query
        cursor.execute(sql, val)
        conn.commit()

    except Exception as e:
        print(f"Error updating login and ping status: {e}")

# Function to update camera status
def update_camera_status(data, cursor, conn, ip_address):
    try:
        detail_infos = data['Response']['Data']['DetailInfos']

        for camera in detail_infos:
            camera_id = camera['ID']
            camera_name = f"Camera_{camera_id}"
            if camera_id in [1, 2, 3, 4]:
                status = 'Working' if camera['Status'] == 1 else 'Not Working'

                # Prepare SQL query to update the Camera status
                sql = f"UPDATE sites_master SET {camera_name} = %s, updated_at = NOW() WHERE ip_address = %s"
                val = (status, ip_address)

                # Debugging: Print the SQL query and values
                print(f"Executing SQL: {sql} with values {val}")

                # Execute SQL query
                cursor.execute(sql, val)
                conn.commit()

                # Print camera status
                print(f"{camera_name}: {status}")

        return True

    except Exception as e:
        print(f"Error updating camera status: {e}")
        return False

# Function to update HDD status
def update_hdd_status(data, cursor, conn, ip_address):
    try:
        local_hdd_list = data['Response']['Data']['LocalHDDList']

        for hdd in local_hdd_list:
            if hdd['ID'] == 1:
                status = 'Working' if hdd['Status'] == 3 else 'Not Working'

                # Prepare SQL query to update the HDD status
                sql = "UPDATE sites_master SET HDD_Status = %s, updated_at = NOW() WHERE ip_address = %s"
                val = (status, ip_address)

                # Debugging: Print the SQL query and values
                print(f"Executing SQL: {sql} with values {val}")

                # Execute SQL query
                cursor.execute(sql, val)
                conn.commit()

                # Print HDD status
                print(f"HDD_Status: {status}")

        return True

    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False

# Function to fetch camera status with timeout
def fetch_camera_status(endpoint, username, password, timeout=10):
    try:
        # HTTP Digest Authentication
        auth = HTTPDigestAuth(username, password)

        # GET request with Digest Auth and timeout
        response = requests.get(endpoint, auth=auth, timeout=timeout)

        # Check for HTTP errors
        response.raise_for_status()

        return response.json()  # Return JSON content

    except requests.exceptions.Timeout as timeout_err:
        print(f'Request timed out: {timeout_err}')
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to fetch HDD status with timeout
def fetch_hdd_status(endpoint, username, password, timeout=10):
    try:
        # HTTP Digest Authentication
        auth = HTTPDigestAuth(username, password)

        # GET request with Digest Auth and timeout
        response = requests.get(endpoint, auth=auth, timeout=timeout)

        # Check for HTTP errors
        response.raise_for_status()

        return response.json()  # Return JSON content

    except requests.exceptions.Timeout as timeout_err:
        print(f'Request timed out: {timeout_err}')
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to update database with fetched data
def update_database():
    try:
        # Establish database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch all UNV DVRs
        cursor.execute("SELECT ip_address, Username, Password, port FROM sites_master WHERE DVR_name = 'UNV'")
        dvr_list = cursor.fetchall()

        for dvr in dvr_list:
            ip_address = dvr[0]
            username = dvr[1]
            password = dvr[2]
            port = dvr[3]

            # URLs for endpoints
            camera_status_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/Channels/System/ChannelDetailInfos'
            hdd_status_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/Storage/Containers/DetailInfos'

            # Ping the IP address
            ping_status = 'Working' if ping_ip(ip_address) else 'Not Working'
            login_status = 'Not Working'

            # Update Login_Status and Ping in the database
            update_login_ping_status(cursor, conn, ip_address, login_status, ping_status)

            if ping_status == 'Working':
                # Fetch data from endpoints with timeout
                camera_data = fetch_camera_status(camera_status_endpoint, username, password)
                hdd_data = fetch_hdd_status(hdd_status_endpoint, username, password)

                # Update Camera status in database
                if camera_data:
                    update_camera_status(camera_data, cursor, conn, ip_address)
                    login_status = 'Working'

                # Update HDD status in database
                if hdd_data:
                    update_hdd_status(hdd_data, cursor, conn, ip_address)
                    login_status = 'Working'

            # Update Login_Status again after fetching data
            update_login_ping_status(cursor, conn, ip_address, login_status, ping_status)

        # Close database connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

# Execute the update function
update_database()
