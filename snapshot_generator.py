import av
import time
import logging
import re
import pandas as pd

logging.basicConfig(level=logging.INFO)

SECONDS_TO_SLEEP = 1 * 10
OUTPUT_FOLDER = 'output_images/'

def decode_on_frame_and_save_to_disk(url, filename):
    logging.info(f'Trying to connect to {url}')
    
    try:
        video = av.open(url, 'r', options={'rtsp_transport': 'tcp'})  # Use TCP transport for RTSP
    except av.AVError as e:
        logging.error(f'Failed to connect to {url}: {e}')
        return

    ip_address = extract_ip_from_url(url)
    if ip_address is None:
        logging.error(f'Failed to extract IP address from URL: {url}')
        video.close()
        return

    try:
        for packet in video.demux():
            for frame in packet.decode():
                ts = time.strftime("%Y%m%d-%H%M%S")
                image_filename = f'{OUTPUT_FOLDER}{filename}-{ts}.jpg'
                logging.info(f'Saving Frame {image_filename}')
                frame.to_image(format='rgb24').save(image_filename)

                logging.info('Closing Connection')
                video.close()
                return
    except av.AVError as e:
        logging.error(f'Error during frame capture: {e}')
        video.close()

def extract_ip_from_url(url):
    match = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    if match:
        return match.group(0)
    return None

def read_urls_from_excel(excel_file_path):
    try:
        df = pd.read_excel(excel_file_path)

        if 'URL' in df.columns and 'Filename' in df.columns:
            url_filename_pairs = [(row['URL'], row['Filename']) for _, row in df.iterrows()]
            return url_filename_pairs
        else:
            return None
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return None

if __name__ == "__main__":
    try:
        logging.info('Start Snapshot Generator')
        excel_file_path = 'rtsp_urls.xlsx'  # Replace with your Excel file path

        url_filename_pairs = read_urls_from_excel(excel_file_path)

        if not url_filename_pairs:
            logging.error('No URLs found in the Excel file. Check the file path and content.')
        else:
            for url, filename in url_filename_pairs:
                try:
                    decode_on_frame_and_save_to_disk(url, filename)
                except Exception as error:
                    logging.error(f'Error processing URL: {url} - {error}')
                logging.info(f'Waiting for the next URL, sleep for {SECONDS_TO_SLEEP} sec')
                time.sleep(SECONDS_TO_SLEEP)
    except Exception as error:
        logging.error(error)
