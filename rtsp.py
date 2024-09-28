import os
import requests
from requests.exceptions import RequestException
import pandas as pd

# Read the Excel file
df = pd.read_excel('urls.xlsx')

# Access the URLs from the 'URL' column
urls = df['URL']

# Create a folder to save images
output_folder = 'images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the URLs and save images
for index, url in enumerate(urls):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there's an HTTP error

        image_name = f'image_{index + 1}.jpg'  # Change this to desired image format
        image_path = os.path.join(output_folder, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.content)

        print(f"Image {image_name} saved.")
    except RequestException as e:
        print(f"An error occurred while fetching URL {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
