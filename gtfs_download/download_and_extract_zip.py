import requests
from bs4 import BeautifulSoup
import urllib.parse
from io import BytesIO
import zipfile
import os
import logging
def format_path(path):
    return path.replace('/', '\\')
def download_and_extract_zip(url,new_gtfs_directory):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href')
            if href.endswith('.zip'):
                zip_url = urllib.parse.urljoin(url, href)
                response_zip = requests.get(zip_url, verify=False)
                if response_zip.status_code == 200:
                    zip_data = BytesIO(response_zip.content)
                    original_folder = os.path.splitext(os.path.basename(href))[0]
                    extraction_directory = os.path.join(new_gtfs_directory, original_folder)

                    os.makedirs(extraction_directory, exist_ok=True)

                    with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                        zip_ref.extractall(extraction_directory)

                    extraction_directory_display = format_path(extraction_directory)
                    href_display = format_path(href.replace('/', '\\'))

                    print(f'Successfully extracted {href_display} to {extraction_directory_display}')
                    # logging.error(f'Successfully extracted {href_display} to {extraction_directory_display}')
                else:
                    logging.error(f'Failed to retrieve data from {zip_url}')
                    # print(f'Failed to retrieve data from {zip_url}')
    else:
        print(f'Failed to retrieve data from {url}')