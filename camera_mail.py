import requests
from requests.auth import HTTPDigestAuth
import mysql.connector
from mysql.connector import Error
import json
import subprocess
from datetime import datetime, timedelta
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'atm_data'
}

# Function to ping an IP address with timeout
def ping_ip(ip_address, timeout=5):
    try:
        command = ["ping", "-n", "1", "-w", str(timeout * 1000), ip_address]
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return response.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Ping timed out for IP address {ip_address}")
        return False
    except Exception as e:
        print(f"Error pinging IP address {ip_address}: {e}")
        return False

# Function to update Login_Status and Ping in the database
def update_login_ping_status(cursor, conn, ip_address, login_status, ping_status):
    try:
        sql = "UPDATE sites_master SET Login_Status = %s, Ping = %s, updated_at = NOW() WHERE ip_address = %s"
        val = (login_status, ping_status, ip_address)
        cursor.execute(sql, val)
        conn.commit()
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
                sql = f"UPDATE sites_master SET {camera_name} = %s, updated_at = NOW() WHERE ip_address = %s"
                val = (status, ip_address)
                cursor.execute(sql, val)
                conn.commit()
                print(f"SQL Update - {camera_name}: {status} for IP: {ip_address}")
        return True
    except Exception as e:
        print(f"Error updating camera status: {e}")
        return False

# Function to update HDD status
def update_hdd_status(data, cursor, conn, ip_address):
    try:
        local_hdd_list = data['Response']['Data']['LocalHDDList']
        hdd1_status = 'Not Working'
        hdd2_status = 'Not Working'
        for hdd in local_hdd_list:
            hdd_id = hdd['ID']
            if hdd_id == 1:
                hdd1_status = 'Working' if hdd['Status'] == 3 else 'Not Working'
            elif hdd_id == 2:
                hdd2_status = 'Working' if hdd['Status'] == 3 else 'Not Working'
        overall_status = 'Working' if (hdd1_status == 'Working' or hdd2_status == 'Working') else 'Not Working'
        sql = "UPDATE sites_master SET HDD_Status = %s, updated_at = NOW() WHERE ip_address = %s"
        val = (overall_status, ip_address)
        cursor.execute(sql, val)
        conn.commit()
        print(f"SQL Update - HDD_Status: {overall_status} for IP: {ip_address}")
        return True
    except Exception as e:
        print(f"Error updating HDD status: {e}")
        return False

# Function to update DVR time status in Indian Standard Time (IST)
def update_dvr_time_status(data, cursor, conn, ip_address):
    try:
        dvr_time_unix = data['Response']['Data']['DeviceTime']
        dvr_time_utc = datetime.utcfromtimestamp(dvr_time_unix)
        ist_offset = timedelta(hours=5, minutes=30)
        dvr_time_ist = dvr_time_utc + ist_offset
        dvr_time_ist_str = dvr_time_ist.strftime('%Y-%m-%d %H:%M:%S')
        sql = "UPDATE sites_master SET DVR_Time = %s, updated_at = NOW() WHERE ip_address = %s"
        val = (dvr_time_ist_str, ip_address)
        cursor.execute(sql, val)
        conn.commit()
        print(f"SQL Update - DVR_Time (IST): {dvr_time_ist_str} for IP: {ip_address}")
        return True
    except Exception as e:
        print(f"Error updating DVR time status: {e}")
        return False

# Function to fetch camera status with timeout
def fetch_camera_status(endpoint, username, password, timeout=10):
    try:
        auth = HTTPDigestAuth(username, password)
        response = requests.get(endpoint, auth=auth, timeout=timeout)
        response.raise_for_status()
        return response.json()
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
        auth = HTTPDigestAuth(username, password)
        response = requests.get(endpoint, auth=auth, timeout=timeout)
        response.raise_for_status()
        return response.json()
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
        auth = HTTPDigestAuth(username, password)
        response = requests.get(endpoint, auth=auth, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as timeout_err:
        print(f'Request timed out: {timeout_err}')
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to gather summary data
def gather_summary(cursor):
    summary = {
        'Camera_1_Not_Working': 0,
        'Camera_2_Not_Working': 0,
        'Camera_3_Not_Working': 0,
        'Camera_4_Not_Working': 0,
        'HDD_Not_Working': 0,
        'Ping_Not_Working': 0,
        'Login_Status_Not_Working': 0
    }

    try:
        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE Camera_1 = 'Not Working'")
        summary['Camera_1_Not_Working'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE Camera_2 = 'Not Working'")
        summary['Camera_2_Not_Working'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE Camera_3 = 'Not Working'")
        summary['Camera_3_Not_Working'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE Camera_4 = 'Not Working'")
        summary['Camera_4_Not_Working'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE HDD_Status = 'Not Working'")
        summary['HDD_Not_Working'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE Ping = 'Not Working'")
        summary['Ping_Not_Working'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sites_master WHERE Login_Status = 'Not Working'")
        summary['Login_Status_Not_Working'] = cursor.fetchone()[0]

    except Exception as e:
        print(f"Error gathering summary data: {e}")

    return summary

# Function to generate dashboard Excel file
def generate_dashboard(cursor):
    try:
        cursor.execute("SELECT * FROM sites_master")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=columns)
        file_path = 'dashboard.xlsx'
        df.to_excel(file_path, index=False)
        print(f"Dashboard Excel file created: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        return None

# Function to send email
def send_email(summary, file_path, recipient_email):
    try:
        sender_email = "rohitb@comforttechno.com"
        sender_password = "Css@ctrb121"
        subject = "DVR Status Summary and Dashboard"

        # Create email content
        body = (f"Summary:\n"
                f"Camera 1 Not Working: {summary['Camera_1_Not_Working']}\n"
                f"Camera 2 Not Working: {summary['Camera_2_Not_Working']}\n"
                f"Camera 3 Not Working: {summary['Camera_3_Not_Working']}\n"
                f"Camera 4 Not Working: {summary['Camera_4_Not_Working']}\n"
                f"HDD Not Working: {summary['HDD_Not_Working']}\n"
                f"Ping Not Working: {summary['Ping_Not_Working']}\n"
                f"Login Status Not Working: {summary['Login_Status_Not_Working']}")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach the dashboard file
        with open(file_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name='dashboard.xlsx')
        part['Content-Disposition'] = 'attachment; filename="dashboard.xlsx"'
        msg.attach(part)

        # Send the email
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")

    except Exception as e:
        print(f"Error sending email: {e}")

# Function to update database with fetched data
def update_database():
    try:
        with open('ip_addresses.txt', 'r') as file:
            ip_addresses = file.read().splitlines()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for ip_address in ip_addresses:
            cursor.execute("SELECT Username, Password, port FROM sites_master WHERE ip_address = %s AND DVR_name = 'UNV'", (ip_address,))
            result = cursor.fetchone()

            if result:
                username, password, port = result
                update_dvr(ip_address, username, password, port)

        summary = gather_summary(cursor)
        file_path = generate_dashboard(cursor)
        send_email(summary, file_path, "rohitb@comforttechno.com")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

# Function to update DVR details
def update_dvr(ip_address, username, password, port):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        ping_status = 'Working' if ping_ip(ip_address) else 'Not Working'
        login_status = 'Not Working'
        update_login_ping_status(cursor, conn, ip_address, login_status, ping_status)

        if ping_status == 'Working':
            camera_status_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/Channels/System/ChannelDetailInfos'
            hdd_status_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/Storage/Containers/DetailInfos'
            dvr_time_endpoint = f'http://{ip_address}:{port}/LAPI/V1.0/System/Time'

            camera_data = fetch_camera_status(camera_status_endpoint, username, password)
            hdd_data = fetch_hdd_status(hdd_status_endpoint, username, password)
            dvr_time_data = fetch_dvr_time_status(dvr_time_endpoint, username, password)

            if camera_data:
                update_camera_status(camera_data, cursor, conn, ip_address)
                login_status = 'Working'
            if hdd_data:
                update_hdd_status(hdd_data, cursor, conn, ip_address)
                login_status = 'Working'
            if dvr_time_data:
                update_dvr_time_status(dvr_time_data, cursor, conn, ip_address)
                login_status = 'Working'
        else:
            cursor.execute("UPDATE sites_master SET Camera_1 = NULL, Camera_2 = NULL, Camera_3 = NULL, Camera_4 = NULL, HDD_Status = NULL, Login_Status = 'Not Working', Ping = 'Not Working', updated_at = NOW() WHERE ip_address = %s", (ip_address,))
            conn.commit()

        update_login_ping_status(cursor, conn, ip_address, login_status, ping_status)
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

# Execute the update function
update_database()
