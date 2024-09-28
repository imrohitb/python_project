import os
import requests
import pandas as pd
import signal
import sys
import time

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Read URLs from a text file
def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file]
        return urls
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

# Process URLs and print status
def process_urls(urls):
    df = pd.DataFrame(columns=['URL', 'Page Size (bytes)', 'Status Code'])
    try:
        for url in urls:
            try:
                response = requests.get(url, timeout=5)  # Add timeout of 5 seconds
                page_size = len(response.content)
                status_code = response.status_code
                print(f"Processed URL: {url} | Status Code: {status_code}")
            except requests.RequestException:
                page_size = None
                status_code = None
                print(f"Error processing URL: {url}")

            df = df._append({
                'URL': url,
                'Page Size (bytes)': page_size,
                'Status Code': status_code
            }, ignore_index=True)

    except KeyboardInterrupt:
        print("\nUser interrupted the process. Saving results and exiting...")
        output_path = os.path.join(script_directory, 'webpage_details.xlsx')
        df.to_excel(output_path, index=False)
        print(f"Webpage details exported to '{output_path}'")
        sys.exit(0)  # Exit gracefully

    return df

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print("\nUser interrupted the process. Saving results and exiting...")
    sys.exit(0)

if __name__ == "__main__":
    file_path = os.path.join(script_directory, "urls.txt")  # Assuming 'urls.txt' is in the same folder
    urls = read_urls_from_file(file_path)
    if urls:
        print("Processing URLs:")
        signal.signal(signal.SIGINT, signal_handler)  # Register Ctrl+C handler
        result_df = process_urls(urls)
        print("\nWebpage details:")
        print(result_df)
        output_path = os.path.join(script_directory, 'webpage_details.xlsx')
        result_df.to_excel(output_path, index=False)
        print(f"\nWebpage details exported to '{output_path}'")
    else:
        print("No URLs found in the file.")
