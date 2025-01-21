import os
from datetime import datetime, timedelta
import shutil

base_dir = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs'

def get_date_str(date):
    return date.strftime('%d%m%y')


def rename_folder(old_name, new_name):
    old_folder_path = os.path.join(base_dir, old_name)
    new_folder_path = os.path.join(base_dir, new_name)
    if os.path.exists(old_folder_path):
        os.rename(old_folder_path, new_folder_path)


def manage_folders(gtfs_weekly_directory):

    # Get today's date
    today = datetime.now()

    # Create a list of folder names for the last 7 days
    folders = [f'gtfs_{get_date_str(today - timedelta(days=i))}' for i in range(8, 0, -1)]
    folders_to_delete=[]
    for folder_name in os.listdir(gtfs_weekly_directory):
        folder_path = os.path.join(gtfs_weekly_directory, folder_name)

        # Check if the current item is a directory
        if os.path.isdir(folder_path):
            # Check if the folder is not in the list of folders to keep
            if folder_name not in folders:
                # try:
                folders_to_delete.append(folder_path)
                # shutil.rmtree(folder_path)  # Delete the folder
                #     print(f"Deleted: {folder_path}")
                # except Exception as e:
                #     print(f"Error deleting {folder_path}: {e}")
    if folders_to_delete:
        for folder in folders_to_delete:
            # os.chmod(folder_path, 0o777)
            shutil.rmtree(folder_path)  # Delete the folder

    # # Rename folders from oldest to newest (shift dates forward)
    # for i in range(len(folders) - 1):
    #     rename_folder(folders[i], "temp" + folders[i + 1][4:])
    #
    # for i in range(len(folders) - 1):
    #     rename_folder("temp" + folders[i], "gtfs" + folders[i][4:])

    # Delete the oldest folder (which now has the second oldest date after renaming)
    oldest_folder_path = os.path.join(base_dir, folders[0])
    if os.path.exists(oldest_folder_path):
        shutil.rmtree(oldest_folder_path)
    # Create a new folder for today's data
    # new_folder_name = f'gtfs_{get_date_str(today)}'
    # new_folder_path = os.path.join(base_dir, new_folder_name)
    # if not os.path.exists(new_folder_path):
    #     os.makedirs(new_folder_path)

    print("Folder renaming, cleanup, and creation complete.")