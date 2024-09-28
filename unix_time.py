import requests
from datetime import datetime, timedelta
from requests.auth import HTTPDigestAuth

# DVR's IP and API endpoint
url = "http://10.126.36.55:81/LAPI/V1.0/Channels/1/Media/Video/Streams/1/Records"

# Authentication details
username = "admin"
password = "admin123"

# Calculate the Begin and End timestamps for the last 90 days
now = datetime.utcnow()
end_time = int(now.timestamp())  # Current time in Unix timestamp
begin_time = int((now - timedelta(days=120)).timestamp())  # 90 days ago in Unix timestamp

# Print the timestamps to ensure they are correct
print(f"Begin Time (90 days ago): {datetime.utcfromtimestamp(begin_time).strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"End Time (Now): {datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S UTC')}")

# API request parameters
params = {
    'Begin': begin_time,
    'End': end_time
}

# Send the request using Digest Authentication
response = requests.get(url, params=params, auth=HTTPDigestAuth(username, password))

# Print the status code and response content for debugging
print(f"Status Code: {response.status_code}")

# Check if the request was successful
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Print the entire JSON response for debugging
        print("Response JSON:", data)

        # Check if 'RecordInfos' is present and iterate over the recording segments
        if 'Data' in data['Response'] and 'RecordInfos' in data['Response']['Data']:
            for record in data['Response']['Data']['RecordInfos']:
                begin_timestamp = record['Begin']
                end_timestamp = record['End']

                # Convert to readable datetime format
                begin_time_readable = datetime.utcfromtimestamp(begin_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
                end_time_readable = datetime.utcfromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

                # Print the Begin and End times
                print(f"Recording Begin: {begin_time_readable}")
                print(f"Recording End: {end_time_readable}\n")
        else:
            print("No 'RecordInfos' found in the response.")
    except Exception as e:
        print(f"Failed to parse JSON response: {e}")
        print(response.text)
else:
    print(f"Failed to fetch records. Status code: {response.status_code}")
    print(response.text)
