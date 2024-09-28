import requests
from requests.auth import HTTPDigestAuth
import mysql.connector
from mysql.connector import Error
import json
import subprocess
from datetime import datetime, timedelta

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

        # Run the ping command
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

        # Execute SQL query
        cursor.execute(sql, val)
        conn.commit()

        # Print SQL update status
        print(f"SQL Update - Login_Status: {login_status}, Ping: {ping_status} for IP: {ip_address}")

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

                # Execute SQL query
                cursor.execute(sql, val)
                conn.commit()

                # Print SQL update status
                print(f"SQL Update - {camera_name}: {status} for IP: {ip_address}")

        return True

    except Exception as e:
        print(f"Error updating camera status: {e}")
        return False


# Function to update HDD status
def update_hdd_status(data, cursor, conn, ip_address):
    try:
        local_hdd_list = data['Response']['Data']['LocalHDDList']

        # Initialize variables to store the final status for both IDs
        hdd1_status = 'Not Working'
        hdd2_status = 'Not Working'

        # Iterate over each HDD entry
        for hdd in local_hdd_list:
            hdd_id = hdd['ID']
            if hdd_id == 1:
                hdd1_status = 'Working' if hdd['Status'] == 3 else 'Not Working'
            elif hdd_id == 2:
                hdd2_status = 'Working' if hdd['Status'] == 3 else 'Not Working'

        # Determine the overall HDD status for the IP address
        overall_status = 'Working' if (hdd1_status == 'Working' or hdd2_status == 'Working') else 'Not Working'

        # Prepare SQL query to update the HDD status
        sql = "UPDATE sites_master SET HDD_Status = %s, updated_at = NOW() WHERE ip_address = %s"
        val = (overall_status, ip_address)

        # Execute SQL query
        cursor.execute(sql, val)
        conn.commit()

        # Print HDD status update for IP address
        print(f"SQL Update - HDD_Status: {overall_status} for IP: {ip_address}")

        return True

    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False

    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False


    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False


    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False


    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False

# Function to update DVR time status in Indian Standard Time (IST)
def update_dvr_time_status(data, cursor, conn, ip_address):
    try:
        dvr_time_unix = data['Response']['Data']['DeviceTime']

        # Convert Unix time to UTC
        dvr_time_utc = datetime.utcfromtimestamp(dvr_time_unix)

        # Add UTC offset for Indian Standard Time (IST)
        ist_offset = timedelta(hours=5, minutes=30)
        dvr_time_ist = dvr_time_utc + ist_offset

        # Format IST time as string
        dvr_time_ist_str = dvr_time_ist.strftime('%Y-%m-%d %H:%M:%S')

        # Prepare SQL query to update the DVR time status in IST
        sql = "UPDATE sites_master SET DVR_Time = %s, updated_at = NOW() WHERE ip_address = %s"
        val = (dvr_time_ist_str, ip_address)

        # Execute SQL query
        cursor.execute(sql, val)
        conn.commit()

        # Print SQL update status
        print(f"SQL Update - DVR_Time (IST): {dvr_time_ist_str} for IP: {ip_address}")

        return True

    except Exception as e:
        print(f"Error updating DVR time status: {e}")
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

# Function to fetch DVR time status with timeout
def fetch_dvr_time_status(endpoint, username, password, timeout=10):
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

# Function to update database with fetched data for specific IP address
def update_database_for_ip(ip_address):
    try:
        # Establish database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch specific DVR by IP address where DVR_name is UNV
        cursor.execute("SELECT ip_address, Username, Password, port FROM sites_master WHERE ip_address = %s AND DVR_name = 'UNV'", (ip_address,))
        dvr = cursor.fetchone()

        if dvr:
            ip_address = dvr[0]
            username = dvr[1]
            password = dvr[2]
            port = dvr[3]

            # Ping the IP address
            if ping_ip(ip_address):
                ping_status = 'Working'
                login_status = 'Working'

                # Update Login_Status and Ping in the database
                update_login_ping_status(cursor, conn, ip_address, login_status, ping_status)

                # URLs for endpoints
                camera_status_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/Channels/System/ChannelDetailInfos'
                hdd_status_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/Storage/Containers/DetailInfos'
                dvr_time_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/System/Time'

                # Fetch data from endpoints with timeout
                camera_data = fetch_camera_status(camera_status_endpoint, username, password)
                hdd_data = fetch_hdd_status(hdd_status_endpoint, username, password)
                dvr_time_data = fetch_dvr_time_status(dvr_time_endpoint, username, password)

                # Update Camera status in database
                if camera_data:
                    update_camera_status(camera_data, cursor, conn, ip_address)

                # Update HDD status in database
                if hdd_data:
                    update_hdd_status(hdd_data, cursor, conn, ip_address)

                # Update DVR time status in database
                if dvr_time_data:
                    update_dvr_time_status(dvr_time_data, cursor, conn, ip_address)

            else:
                # Update Login_Status and Ping in the database if ping fails
                ping_status = 'Not Working'
                login_status = 'Not Working'
                update_login_ping_status(cursor, conn, ip_address, login_status, ping_status)

        else:
            print(f"No DVR found with IP address {ip_address} and DVR_name 'UNV'")

        # Close cursor and connection
        cursor.close()
        conn.close()

    except Error as e:
        print(f"Database error: {e}")

    except Exception as e:
        print(f"Other error occurred: {e}")

# Run the update_database_for_ip function with specific IP address
update_database_for_ip('172.51.25.27')
