import os
import shutil
from datetime import datetime, timedelta
import hashlib  # Added hashlib for hash-based comparison
import filecmp
import move
import logging
from download_and_extract_zip import download_and_extract_zip

def get_date_str(date):
    return date.strftime('%d%m%y')
today = datetime.now()

url = 'https://gtfs.mot.gov.il/gtfsfiles/'  # Replace with the actual API endpoint URL
# Prompt user for paths
new_gtfs_directory = input(f"Enter the new GTFS directory path ")
# Join the user input paths with the dynamic folder name
new_gtfs_directory = os.path.join(new_gtfs_directory, f'gtfs_{get_date_str(today)}')

print("New GTFS Directory:", new_gtfs_directory)
# Define the target directories for saving old and new data within your user directory
# gtfs_directory = fr'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs\gtfs_{get_date_str(today - timedelta(days=1))}'
# new_gtfs_directory = fr'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs\gtfs_{get_date_str(today)}'

# Ensure the old and new target directories exist; create them if they don't
# gtfs_weekly_directory = gtfs_directory[:gtfs_directory.rfind('\\')]


os.makedirs(new_gtfs_directory, exist_ok=True)


def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
download_and_extract_zip(url,new_gtfs_directory)
print(f"Contents of new gtfs downloaded Successfully to gtfs directory: {new_gtfs_directory}.")
# logging.error("Contents of new_gtfs copied to gtfs directory.")
input("Press Enter to exit...")
