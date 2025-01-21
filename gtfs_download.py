import requests
import zipfile
from io import BytesIO
import os
from bs4 import BeautifulSoup
import urllib.parse
import shutil
import datetime
import hashlib  # Added hashlib for hash-based comparison
import filecmp
# import difflib
# Disable SSL certificate verification
requests.packages.urllib3.disable_warnings()

url = 'https://gtfs.mot.gov.il/gtfsfiles/'  # Replace with the actual API endpoint URL

# Define the target directories for saving old and new data within your user directory
gtfs_directory = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\gtfs'
new_gtfs_directory = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\newgtfs'
# gtfs_directory = r'C:\Users\AvichayKadosh\OneDrive - ברשאי\ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\check\old'
# new_gtfs_directory = r'C:\Users\AvichayKadosh\OneDrive - ברשאי\ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\check\new'
# Ensure the old and new target directories exist; create them if they don't
os.makedirs(gtfs_directory, exist_ok=True)
os.makedirs(new_gtfs_directory, exist_ok=True)

# Define the full path for the change log file in the newgtfs folder
# log_file = 'change_log.txt'
# change_log_path = os.path.join(new_gtfs_directory+"\\logs", log_file)
change_log_path = os.path.join(new_gtfs_directory, "logs")
# Initialize the log file handler
# log_file_handler = None

# # Create the log file if it doesn't exist
# if not os.path.exists(change_log_path):
#     open(change_log_path, 'w', encoding='utf-8').close()

# Function to get the current date and time
def get_current_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_path(path):
    return path.replace('/', '\\')

def calculate_file_hash(file_path):
    hasher = hashlib.sha256()  # You can choose a different hash algorithm if needed

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(8192)  # Read the file in chunks
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()
def compare_text_files_using_sets(file1_path, file2_path, relative_path):
    basename=os.path.basename(file1_path)
    print(f"run compare_text_files {basename}")
    basename_without_suffix, _ = os.path.splitext(basename)

    missing_lines = []
    extra_lines = []
    first_row=[]
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        first_row=file1.readline()
        file1.seek(0)  # Move the file pointer back to the beginning
        lines_file1 = [line.strip() for line in file1.readlines()]
        lines_file2 = [line.strip() for line in file2.readlines()]

    set_file1 = set(lines_file1)
    set_file2 = set(lines_file2)

    missing_lines = list(set_file1 - set_file2)
    extra_lines = list(set_file2 - set_file1)
    if missing_lines or extra_lines:
        # Create the log file if it doesn't exist
        full_path = os.path.join(change_log_path, basename_without_suffix + "_change_log.txt")
        if not os.path.exists(full_path):
            open(full_path, 'w', encoding='utf-8').close()
        # log_file_handler = open(full_path , 'a', encoding='utf-8')
        if missing_lines:
            log_changes(f"[{get_current_datetime()}] Missing rows in {relative_path}:\n",full_path)
            log_changes(f'                        {first_row}', full_path)
            for line in missing_lines:
                log_changes(f'                      - {line}\n',full_path)

        if extra_lines:
            log_changes(f"[{get_current_datetime()}] Extra rows in {relative_path}:\n",full_path)
            log_changes(f'                        {first_row}', full_path)
            for line in extra_lines:
                log_changes(f'                      + {line}\n',full_path)
    print(f"finish compare {os.path.basename(file2_path)}")
def compare_text_files(file1_path, file2_path, relative_path):
    print(f"run compare_text_files {os.path.basename(file1_path)}")

    missing_lines = []
    extra_lines = []

    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        lines_file1 = file1.readlines()
        lines_file2 = file2.readlines()

        i = 0
        j = 0

        while i < len(lines_file2) and j<len(lines_file1):
            stripped_line1 = lines_file1[j].strip()
            stripped_line2 = lines_file2[i].strip()

            if stripped_line1 != stripped_line2:
                # Line from file2 not found in file1
                found_in_file1 = False
                # Search in missing_lines
                found_in_missing = False
                for line in missing_lines:
                    if line.strip() == stripped_line2:
                        found_in_missing = True
                        missing_lines.remove(line)
                        j-=1
                        break

                if not found_in_missing:
                    # Search for the line in file1
                    for m in range(j,len(lines_file1)):
                        line_in_lines_file1 = lines_file1[m].strip();
                        if line_in_lines_file1 == stripped_line2:
                            found_in_file1 = True
                    if found_in_file1:
                        for k in range(j, len(lines_file1)):
                            line_in_lines_file1 = lines_file1[k].strip();
                            if line_in_lines_file1 == stripped_line2:
                                found_in_file1 = True
                                j = k  # Move j to the next position in file2
                                break
                            missing_lines.append(line_in_lines_file1)

                    if not found_in_file1:
                        missing_lines.append(stripped_line1)
                        extra_lines.append(stripped_line2)
            j+=1
            i += 1
        while i< len (lines_file2):
            line_in_lines_file2 = lines_file2[i].strip();
            extra_lines.append((line_in_lines_file2))
            i+=1
        while j < len(lines_file1):
            line_in_lines_file1 = lines_file1[j].strip();
            missing_lines.append(line_in_lines_file1)
            j+=1
        # Process any remaining lines in missing_lines
        # for line in missing_lines:
        #     extra_lines.append(line.strip())

    if missing_lines:
        log_changes(f"[{get_current_datetime()}] Missing lines in {relative_path}:\n")
        for line in missing_lines:
            log_changes(f'                      -   {line}')

    if extra_lines:
        log_changes(f"[{get_current_datetime()}] Extra lines in {relative_path}:\n")
        for line in extra_lines:
            log_changes(f'                      + {line}')
    close_log_file(log_file_handler)
    print(f"finish compare {os.path.basename(file2_path)}")
# def compare_text_files(file1_path, file2_path,relative_path):
#     print(f"run compare_text_files {os.path.basename(file1_path)}")
#
#     with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
#         lines1 = set(line.strip() for line in file1)
#
#         # Check lines from file1 against file2
#         for line_number, line in enumerate(file2, start=1):
#             stripped_line = line.strip()
#             if stripped_line not in lines1:
#                 log_changes(f"[{get_current_datetime()}] Change in {relative_path} at line {line_number}:\n")
#                 log_changes(f'  File 1: Missing line\n')
#                 log_changes(f'  File 2: {stripped_line}\n')
#
#     print(f"finish compare {os.path.basename(file1_path)}")

# def compare_text_files(file1_path, file2_path, relative_path):
#     print("run compare_text_files " + os.path.basename(file1_path))
#
#     # Check if the relative_path corresponds to a calendar file
#     if os.path.basename(file1_path) == "calendar.txt":
#         # Define the columns to exclude for calendar files
#         excluded_columns = {'start_date', 'end_date'}
#     else:
#         excluded_columns = set()  # Exclude no columns for other files
#
#     with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
#         file1_lines = set(file1.readlines())
#         file2_lines = set(file2.readlines())
#
#     # Lines present in file1 but not in file2
#     lines_only_in_file1 = file1_lines - file2_lines
#
#     # Lines present in file2 but not in file1
#     lines_only_in_file2 = file2_lines - file1_lines
#
#     # Combine both sets of lines
#     diff_lines = lines_only_in_file1.union(lines_only_in_file2)
#
#     if diff_lines:
#         log_changes(f'[{get_current_datetime()}] Changes in {relative_path}:\n')
#         for line in diff_lines:
#             log_changes(f'  {line.strip()}')
#
#     print("finish compare " + os.path.basename(file1_path))

# def compare_text_files(file1_path, file2_path, relative_path):
#     print("run compare_text_files " + os.path.basename(file1_path))
#
#     # Check if the relative_path corresponds to a calendar file
#     if os.path.basename(file1_path) == "calendar.txt":
#         # Define the columns to exclude for calendar files
#         excluded_columns = {'start_date', 'end_date'}
#     else:
#         excluded_columns = set()  # Exclude no columns for other files
#
#     with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
#         file1_lines = file1.readlines()
#         file2_lines = file2.readlines()
#
#     # Initialize a list to store the differences
#     diff_lines = []
#
#     # Find the indexes of 'start_date' and 'end_date' columns (assuming they exist in the header)
#     header_columns1 = file1_lines[0].strip().split(',')
#     header_columns2 = file2_lines[0].strip().split(',')
#
#     start_date_index = None
#     end_date_index = None
#
#     for i, col in enumerate(header_columns1):
#         if col in excluded_columns:
#             start_date_index = i
#             end_date_index = i+1
#             break
#
#     # Iterate through the lines in the files
#     for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
#         # Skip the header row
#         if i == 0:
#             continue
#
#         # Split the lines into columns
#         columns1 = line1.strip().split(',')
#         columns2 = line2.strip().split(',')
#
#         # Ignore the 'start_date' and 'end_date' columns based on their indexes
#         if start_date_index is not None:
#             columns1[start_date_index] = ''
#             columns2[start_date_index] = ''
#         if end_date_index is not None:
#             columns1[end_date_index] = ''
#             columns2[end_date_index] = ''
#
#         # Check if all non-excluded columns are the same
#         if all(columns1[i] == columns2[i] for i in range(len(columns1)) if
#                columns1[i].strip() and columns2[i].strip()):
#             continue  # Skip this line if the non-excluded columns are the same
#
#         # If the line is different or contains excluded columns, add it to the differences list
#         diff_lines.append(f'- {line1}')
#         diff_lines.append(f'+ {line2}')
#
#     if diff_lines:
#         log_changes(f'[{get_current_datetime()}] Changes in {relative_path}:\n{"".join(diff_lines)}')
#     print("finish compare " + os.path.basename(file1_path))


def log_changes(message,full_path):
    # global log_file_handler
    log_file_handler = open(full_path, 'a', encoding='utf-8')
    # Close the existing log file handler (if any)
    # if log_file_handler is not None:
    #     log_file_handler.close()

    # log_file_handler = open(change_log_path, 'a', encoding='utf-8')
    log_file_handler.write(f'{message}')
    log_file_handler.close()

def close_log_file(log_file_handler):
    # global log_file_handler

    if log_file_handler is not None:
        log_file_handler.close()
        log_file_handler = None

def download_and_extract_zip(url):
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
                else:
                    print(f'Failed to retrieve data from {zip_url}')
    else:
        print(f'Failed to retrieve data from {url}')

download_and_extract_zip(url)

# Compare files after extracting all
for root, _, files in os.walk(gtfs_directory):
    if os.path.basename(root) == 'logs':  # Check if the current directory is 'logs'
        t=0
    else:  # Check if the current directory is 'logs'
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), gtfs_directory)
            new_file_path = os.path.join(new_gtfs_directory, relative_path)
            file_name=file[:-4]
            if(file_name != 'calendar' and file_name != 'shapes' and file_name!= 'stop_times'  ):
                if os.path.exists(new_file_path):
                    # Compare files using hash-based comparison
                    hash1 = calculate_file_hash(os.path.join(gtfs_directory, relative_path))
                    hash2 = calculate_file_hash(new_file_path)

                    # if hash1 != hash2:
                    #     compare_text_files(
                    #         os.path.join(gtfs_directory, relative_path),
                    #         new_file_path,
                    #         relative_path
                    #     )

                    if hash1 != hash2:
                        compare_text_files_using_sets(
                            os.path.join(gtfs_directory, relative_path),
                            new_file_path,
                            relative_path
                        )

# Compare directories after extracting all
directory_comparison = filecmp.dircmp(gtfs_directory, new_gtfs_directory)
if not os.path.exists(change_log_path+ "directory"+"_change_log"):
    open(change_log_path+ "directory"+"_change_log", 'w', encoding='utf-8').close()
log_file_handler = open(os.path.join(change_log_path, "directory"+"_change_log"), 'a', encoding='utf-8')


def log_directory_differences(dcmp,full_path):
    for name in dcmp.left_only:
        log_changes(f'[{get_current_datetime()}] New file or directory: {name}\n',full_path)
    for name in dcmp.right_only:
        log_changes(f'[{get_current_datetime()}] File or directory deleted: {name}\n',full_path)
    for name in dcmp.diff_files:
        log_changes(f'[{get_current_datetime()}] Difference in file: {name}\n',full_path)
    for sub_dcmp in dcmp.subdirs.values():
        log_directory_differences(sub_dcmp,full_path)
full_path= os.path.join(change_log_path, "files" + "_change_log.txt")
log_directory_differences(directory_comparison,full_path)

# Copy the content of new_gtfs to gtfs (overwrite existing files)
shutil.rmtree(gtfs_directory)  # Remove the old content of gtfs
shutil.copytree(new_gtfs_directory, gtfs_directory)

print("Contents of new_gtfs copied to gtfs directory.")
# Close the log file
# close_log_file()
