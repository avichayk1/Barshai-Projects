import os
from openpyxl import load_workbook
import pandas as pd
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import datetime

# Define the directory containing Excel files
directory = r'C:\Users\AvichayKadosh\ברשאי\טכנולוגיה - Documents\שירותים\בקרות שטח\בקרות מסע לקוח\03- בדיקות\טפסי בדיקה'
stpos_file_path = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\gtfs\israel-public-transportation\stops.txt'
output_file_path=r'C:\Users\AvichayKadosh\ברשאי\טכנולוגיה - Documents\שירותים\בקרות שטח\בקרות מסע לקוח\03- בדיקות\תוצאות בדיקה'
masaot_path=r'C:\Users\AvichayKadosh\ברשאי\טכנולוגיה - Documents\שירותים\בקרות שטח\בקרות מסע לקוח\04 - מיפוי סיפורי מסע לקוח\רשימת מסעות לקוח.xlsx'
df_stops = pd.read_csv(stpos_file_path)
df_masaot_list=pd.read_excel(masaot_path)
df_masaot_list = df_masaot_list[(df_masaot_list['תאריך בדיקה'] != '0') & (df_masaot_list['תאריך בדיקה'].notnull())]

# Convert the 'תאריך בדיקה' column to datetime.date type

# Function to prompt the user to decide whether to apply filtering or not using a checkbox
def prompt_filtering():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show pop-up dialog to ask the user whether to apply filtering
    #result=messagebox.askquestion("Confirm", "Are you sure?")

    result = simpledialog.askstring("Apply Filtering", "Do you want to apply filtering on the data?[YES,NO]")
    return result == 'YES'

def prompt_executing_date():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show pop-up dialog to get user input
    executing_date = simpledialog.askstring("executing date", "Enter the executing date : XXXX-XX-XX (YEAR-MONTH-DAY) ")
    #root.mainloop()
    # Split user input by comma and remove leading/trailing spaces
    return executing_date

def prompt_executing_name():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show pop-up dialog to get user input
    executing_name = simpledialog.askstring("executing name", "Enter the executing name : ")

    # Split user input by comma and remove leading/trailing spaces
    return executing_name
# Function to prompt the user to enter the filenames to join using a pop-up window
def prompt_filenames():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show pop-up dialog to get user input
    user_input = simpledialog.askstring("File Names","Enter the filenames to join (separated by comma): ")

    # Split user input by comma and remove leading/trailing spaces
    filenames = [filename.strip() for filename in user_input.split(',')]
    return filenames

# Function to prompt the user to enter the postfix using a pop-up window
def prompt_postfix():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show pop-up dialog to get user input
    postfix = simpledialog.askstring("Enter Postfix", "Enter the postfix to concatenate: ")
    return postfix

# Function to prompt the user to enter the output file name using a pop-up window
def prompt_output_filename():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show pop-up dialog to get user input
    output_filename = simpledialog.askstring( "Output File Name","Enter the name of the output file: ")
    return output_filename

def makatByDateAndName(checkDate,checkName):
    # Filter the DataFrame to find the row with the specified stop code and retrieve the stop name
    # x= df_masaot_list['תאריך בדיקה'][0].dt.date.astype(str)
    # Ensure 'תאריך בדיקה' is in datetime format
    df_masaot_list['תאריך בדיקה'] = pd.to_datetime(df_masaot_list['תאריך בדיקה'])

    # Extract the date part for comparison
    df_masaot_list['date_only'] = df_masaot_list['תאריך בדיקה'].dt.date.astype(str)

    # Convert checkDate to string if it is a datetime object
    if isinstance(checkDate, (pd.Timestamp, datetime.date)):
        checkDate = checkDate.strftime('%Y-%m-%d')
    if checkName=='Ram Asaad':
        x=1
    # Filter the DataFrame to find the row with the specified name and date
    result = df_masaot_list.loc[
        (df_masaot_list['שם הבודק'] == checkName) &
        (df_masaot_list['date_only'] == checkDate),
        'מק"ט מסע'
    ].values

    # Return the first result if it exists, else return None
    if len(result) > 0:
        x=result[0].astype(int)
        return result[0].astype(int)
    else:
        return 0
def stationNameByMakat(makat):
    # Filter the DataFrame to find the row with the specified stop code and retrieve the stop name
    result = df_stops.loc[df_stops['stop_code'] == makat, 'stop_name'].values

    if len(result) > 0:
        stop_name = result[0]  # Get the stop name from the first element of the array
        return stop_name
    else:
            return ''
    # Copy header and footer from source document to target document
    # for source_section, target_section in zip(source_doc.sections, target_doc.sections):
    #     if source_section.header is not None:
    #         target_section_header = target_section.header
    #         for source_header_paragraph in source_section.header.paragraphs:
    #             target_section_header.add_run(source_header_paragraph.text)
    #     if source_section.footer is not None:
    #         target_section_footer = target_section.footer
    #         for source_footer_paragraph in source_section.footer.paragraphs:
    #             target_section_footer.add_run(source_footer_paragraph.text)


# Function to filter the DataFrame based on values in the "שם" and "שעת התחלה" columns
def filter_dataframe(df, desired_name, desired_start_date):
    # Extract date component from the datetime column
    # Assuming df['שעת התחלה'] contains timestamps in string format
    # Convert timestamp strings to datetime objects
    df['שעת התחלה'] = pd.to_datetime(df['שעת התחלה'])    # Filter the DataFrame based on the desired criteria
    # Extract date part from datetime objects and convert them to string
    df['שעת התחלה_date'] = df['שעת התחלה'].dt.date.astype(str)
    filtered_df = df[(df['שם'] == desired_name) & ((pd.to_datetime(df['שעת התחלה'])).dt.date.astype(str) == desired_start_date)]
    return filtered_df

user_filter=prompt_filtering()
# Prompt the user to enter the filenames to join
# file_names = prompt_filenames()

# Prompt the user to enter the name of the output file
# output_file_name = prompt_output_filename()
output_file_name_shelet= "ריכוז שלטים"
output_file_name_masof="ריכוז מסופים"
output_file_name_nesia="ריכוז נסיעות ברכב"
# Keywords to search for in the columns
keywords = ['לא תקין', 'לא נבדק', 'תקין']
if(user_filter):
    executing_name=prompt_executing_name()
    executing_date=prompt_executing_date()

# Initialize an empty list to store the DataFrames
dfs_ahelet = []
dfs_masof = []
dfs_nesia = []
# # Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".xlsx") and filename != 'סיכום.xlsx' and filename != 'ריכוז שלטים.xlsx' and filename !="ריכוז מסופים.xlsx" and filename !="ריכוז נסיעות ברכב.xlsx":  # Skip the output file
        # Read each Excel file into a DataFrame
        file_path = os.path.join(directory, filename)
        # df = pd.read_excel(file_path, sheet_name='Form1', index_col=None)
        df = pd.read_excel(file_path,sheet_name="Form1", index_col=None)
        if 'Start time' in df.columns:
            df.rename(columns={'Start time': 'שעת התחלה'}, inplace=True)
        if 'Name' in df.columns:
            df.rename(columns={'Name': 'שם'}, inplace=True)
        if 'Completion time' in df.columns:
            df.rename(columns={'Completion time': 'שעת השלמה'}, inplace=True)
        if 'Email' in df.columns:
            df.rename(columns={'Email': 'דואר אלקטרוני'}, inplace=True)
        if 'Last modified time' in df.columns:
            df.rename(columns={'Last modified time': 'מועד שינוי אחרון'}, inplace=True)
        # Drop the ID column
        # df = df.drop(columns=['ID'])

        # Append the DataFrame to the list
        if (user_filter):
            filtered_df = filter_dataframe(df, executing_name+" Barshai LTD", executing_date)
            if(filename.startswith("שלט")):
                dfs_ahelet.append(filtered_df)
            elif(filename.startswith("מסופים")):
                dfs_masof.append(filtered_df)
            elif(filename.startswith("נסיעה")):
                dfs_masof.append(filtered_df)
        else:
            if (filename.startswith("שלט")):
                dfs_ahelet.append(df)
            elif (filename.startswith("מסופים") or filename.startswith("תחנה")):
                dfs_masof.append(df)
            elif (filename.startswith("נסיעה")):
                dfs_nesia.append(df)

##code for choose files
# # Loop through each specified file
# for filename in file_names:
#     file_path = os.path.join(directory, filename+ '.xlsx')
#     if os.path.exists(file_path):
#         # Read the Excel file into a DataFrame
#         df = pd.read_excel(file_path, index_col=None)
#
#         if(user_filter):
#             filtered_df = filter_dataframe(df, executing_name+" Barshai LTD", executing_date)
#             dfs.append(filtered_df)
#         else:
#             dfs.append(df)
#     else:
#         print(f"File '{filename}' not found in directory.")

# Perform join operation if there are DataFrames to join
# if dfs_ahelet:
#     # Join DataFrames
#     joined_df = pd.concat(dfs_ahelet, axis=0, ignore_index=True)
#     if 'שם תחנה' not in joined_df.columns:
#         joined_df.insert(joined_df.columns.get_loc('מק"ט תחנה') + 1, 'שם תחנה', joined_df['מק"ט תחנה'].apply(lambda x: stationNameByMakat(x)))
#     # Order by Date and Time
#     joined_df['שעת התחלה'] = pd.to_datetime(joined_df['שעת התחלה'])
#     joined_df = joined_df.sort_values(by='שעת התחלה')
#     # Write the joined DataFrame to a new Excel file in the same directory, overriding if exists
#     output_file = os.path.join(directory, output_file_name+ '.xlsx')
#     # columns_containing_invalid =joined_df[joined_df.apply(lambda row: any("לא תקין" in val for val in row), axis=1)]
#     # List to store indices of invalid rows
#     invalid_indices = []
if dfs_ahelet:
    # Join DataFrames
    joined_df = pd.concat(dfs_ahelet, axis=0, ignore_index=True)

    # Add 'שם תחנה' column if it does not exist
    if 'שם תחנה' not in joined_df.columns:
        joined_df.insert(joined_df.columns.get_loc('מק"ט תחנה') + 1, 'שם תחנה',
                         joined_df['מק"ט תחנה'].apply(lambda x: stationNameByMakat(x)))

    # Convert 'שעת התחלה' to datetime
    joined_df['שעת התחלה'] = pd.to_datetime(joined_df['שעת התחלה'])

    # Sort by 'שעת התחלה'
    joined_df = joined_df.sort_values(by='שעת התחלה')

    # # Create a unique key by combining 'שם' and the date part of 'שעת התחלה'
    # joined_df['unique_key'] = joined_df['שם'] + '_' + joined_df['שעת התחלה'].dt.date.astype(str)
    #
    # # Generate a 'trip_id' for each unique key
    # joined_df['temp_group_id'] = joined_df.groupby('unique_key').ngroup() + 1

    # joined_df['masa_id'] = joined_df.groupby('unique_key').ngroup() + 1
    # joined_df['masa_id'] = joined_df.apply(
    #     lambda row: makatByDateAndName(
    #         row['שעת התחלה'],
    #         row['שם'][:-12] if row['שם'].endswith('Barshai LTD') else row['שם']
    #     ),
    #     axis=1
    # )
    # Initialize an empty list to store the results
    masa_ids = []

    # Iterate over each row in the DataFrame
    for index, row in joined_df.iterrows():
        # print(row)
        # Check the condition and process the 'שם' column accordingly
        if 'שם' in joined_df.columns:
            name_processed = row['שם'][:-12] if row['שם'].endswith('Barshai LTD') else row['שם']
        elif 'Name' in joined_df.columns:
            name_processed = row['Name'][:-12] if row['Name'].endswith('Barshai LTD') else row['Name']
        print(row['סוג בדיקה'],name_processed,row['שעת התחלה'],row['מק"ט תחנה'])
        print(row['שעת התחלה'].strftime('%Y-%m-%d')== '2024-06-04')
        print(row['מק"ט תחנה']==53810)
        if(row['מק"ט תחנה']==53810):
            y=0
        if (row['שעת התחלה'].strftime('%Y-%m-%d')== '2024-06-04'):
            y=9
        if name_processed=='Ram Asaad':
            c=8
        # Call the makatByDateAndName function with the processed name and 'שעת התחלה'
        if 'שעת התחלה' in joined_df.columns:
            masa_id = makatByDateAndName(row['שעת התחלה'], name_processed)
        elif 'Start time' in joined_df.columns:
            masa_id = makatByDateAndName(row['Start time'], name_processed)
        # Append the result to the masa_ids list
        masa_ids.append(masa_id)

    # Assign the list of results to a new column in the DataFrame
    joined_df['masa_id'] = masa_ids
    # # Drop the temporary 'unique_key' column
    joined_df.drop(columns=['ID'], inplace=True)
    # # joined_df.drop(columns=['unique_key'], inplace=True)
    # joined_df.drop(columns=['unique_key', 'temp_group_id'], inplace=True)

    # Ensure the 'trip_id' column is at the start of the DataFrame
    cols = ['masa_id'] + [col for col in joined_df.columns if col != 'masa_id']
    joined_df = joined_df[cols]
    joined_df = joined_df.sort_values(by='masa_id')

    # Write the joined DataFrame to a new Excel file in the same directory, overriding if exists
    output_file = os.path.join(output_file_path, output_file_name_shelet + '.xlsx')
    joined_df.to_excel(output_file, index=False)
    #     filtered_df.to_excel(output_file, index=False)
    for masa_id in joined_df['masa_id'].unique():
        # Create a folder for the current masa_id
        masa_id_folder_name= f'masa_id_{masa_id}'
        masa_id_folder = os.path.join(output_file_path, masa_id_folder_name)
        # Define the output file path
        file_name=f'shlatim masa_id_{masa_id}.xlsx'
        output_file = os.path.join(masa_id_folder, file_name)
        if not os.path.exists(masa_id_folder):
            print(f"New directory: \nDirectory name:{masa_id_folder_name}")
            os.makedirs(masa_id_folder)
        else:
            print(f"the folder: {masa_id_folder_name} already exist")
        if not os.path.exists(output_file):
            print(f"New file: \nFile name: {file_name}\nFile path: {output_file}")
            # Filter the DataFrame for the current masa_id
            filtered_df = joined_df[joined_df['masa_id'] == masa_id]

            # Further filter the DataFrame to include only rows without "לא תקין"
            valid_rows = filtered_df[filtered_df.apply(
                lambda row: any(isinstance(val, str) and "לא תקין" in val for val in row if not pd.isna(val)), axis=1)]
            # Find the starting index of the first column that contains any of the keywords
            start_index = None
            for idx, col in enumerate(valid_rows.columns):
                if valid_rows[col].apply(
                        lambda val: isinstance(val, str) and any(keyword in val for keyword in keywords)).any():
                    start_index = idx
                    break

            if start_index is None:
                continue  # If no such column is found, move to the next masa_id
            # Find triplets of columns where the first column contains "לא תקין"
            columns_to_save = []
            # for i in range(start_index, len(valid_rows.columns), 3):
            #     triplet = valid_rows.columns[i:i + 3]
            #     if valid_rows[triplet[0]].apply(lambda val: isinstance(val, str) and "לא תקין" in val).any():
            #         columns_to_save.extend(triplet)
            i = start_index
            step_size=3

            while i < len(valid_rows.columns):
                tripletx = valid_rows.columns[i]
                if tripletx == "כפתור כריזה":
                    x = 5
                # Alternate the step size between 3 and 2
                if  tripletx == "שפות" or tripletx == 'כפתור כריזה' or tripletx == 'יציאה או הגעה בזמן' or tripletx == 'תיקוף ביישומון' or tripletx == 'ביטחון אישי':
                    step_size = 2
                else:
                    step_size = 3

                # Move to the next set of columns
                if step_size ==2:
                    c=45
                triplet = valid_rows.columns[i:i + step_size]
                i += step_size
                # Ensure the triplet is not empty and has the expected number of columns
                if len(triplet) > 0:
                    # if valid_rows[triplet[0]].apply(lambda val: isinstance(val, str) and "לא תקין" in val).any():
                    #     columns_to_save.extend(triplet)

                    for val in valid_rows[triplet[0]]:
                        if isinstance(val, str):
                            if "לא תקין" in val:
                                columns_to_save.extend(triplet)
                                break

            additional_columns=valid_rows.iloc[:, :start_index]
            # Get the column names up to the start index
            additional_columns = additional_columns.columns.tolist()
            for col in reversed(additional_columns):
                columns_to_save.insert(0, col)
            # Remove duplicates while preserving order
            columns_to_save = list(dict.fromkeys(columns_to_save))

            # Filter the DataFrame to keep only the necessary columns
            valid_rows = valid_rows[columns_to_save]

            # Remove columns that are empty across all rows
            valid_rows = valid_rows.dropna(axis=1, how='all')
            # Save the valid filtered DataFrame to an Excel file
            valid_rows.to_excel(output_file, index=False)
        else:
            print(f"the file: {filename} already exist")
    # List to store indices of invalid rows (if needed in the future)
    # invalid_indices = []  # Iterate over each row in the DataFrame
    # for idx, row in joined_df.iterrows():
    #     # Iterate over each value in the row
    #     for val in row:
    #         # Check if the value is a string and contains "לא תקין"
    #         if isinstance(val, str) and "לא תקין" in val:
    #             # If found, add the index of the row to invalid_indices
    #             invalid_indices.append(idx)
    #             # Break to move to the next row
    #             break
    #
    # # Filter the DataFrame to include only invalid rows
    # invalid_rows = joined_df.loc[invalid_indices]
    # # for col in joined_df.columns
    # # filtered_df = joined_df[joined_df.apply(lambda row: any(isinstance(val, str) and "לא תקין" in val for val in row if not pd.isna(val)), axis=1)]
    # invalid_rows.to_excel(output_file, index=False)
if dfs_masof:
    joined_df = pd.concat(dfs_masof, axis=0, ignore_index=True)
    if 'שם תחנה' not in joined_df.columns:
        joined_df.insert(joined_df.columns.get_loc('מק"ט תחנה') + 1, 'שם תחנה',joined_df['מק"ט תחנה'].apply(lambda x: stationNameByMakat(x)))
    # Order by Date and Time
    joined_df['שעת התחלה'] = pd.to_datetime(joined_df['שעת התחלה'])
    joined_df = joined_df.sort_values(by='שעת התחלה')

    # # Create a unique key by combining 'שם' and the date part of 'שעת התחלה'
    # joined_df['unique_key'] = joined_df['שם'] + '_' + joined_df['שעת התחלה'].dt.date.astype(str)
    #
    # # Generate a 'trip_id' for each unique key
    # joined_df['temp_group_id'] = joined_df.groupby('unique_key').ngroup() + 1
    # joined_df['masa_id'] = joined_df.groupby('unique_key').ngroup() + 1
    # joined_df['masa_id'] = joined_df.apply(lambda row: makatByDateAndName(row['שעת התחלה'].date(), row['שם'][:-12]), axis=1)
    masa_ids = []

    # Iterate over each row in the DataFrame
    for index, row in joined_df.iterrows():
        # print(row)
        # Check the condition and process the 'שם' column accordingly
        if 'שם' in joined_df.columns:
            name_processed = row['שם'][:-12] if row['שם'].endswith('Barshai LTD') else row['שם']
        elif 'Name' in joined_df.columns:
            name_processed = row['Name'][:-12] if row['Name'].endswith('Barshai LTD') else row['Name']
        print(row['סוג בדיקה'], name_processed, row['שעת התחלה'],row['מק"ט תחנה'])
#        print(row['שעת התחלה'] == pd.to_datetime('04/06/2024  17:41:26'))
        print(row['שעת התחלה'].strftime('%Y-%m-%d')== '2024-06-04')
        print(row['מק"ט תחנה']=='53810')
        if(row['מק"ט תחנה']=='53810'):
            y=0
        if (row['שעת התחלה'].strftime('%Y-%m-%d')== '2024-06-04'):
            y = 6
        # if name_processed=='Ram Asaad':
        #     c=8
        # Call the makatByDateAndName function with the processed name and 'שעת התחלה'
        if 'שעת התחלה' in joined_df.columns:
            masa_id = makatByDateAndName(row['שעת התחלה'], name_processed)
        elif 'Start time' in joined_df.columns:
            masa_id = makatByDateAndName(row['Start time'], name_processed)
        # Append the result to the masa_ids list
        masa_ids.append(masa_id)

    # Assign the list of results to a new column in the DataFrame
    joined_df['masa_id'] = masa_ids
    # joined_df['masa_id'] = joined_df.apply(
    #     lambda row: makatByDateAndName(
    #         row['שעת התחלה'],
    #         row['שם'][:-12] if row['שם'].endswith('Barshai LTD') else row['שם']
    #     ),
    #     axis=1
    # )
    # Drop the temporary 'unique_key' column
    joined_df.drop(columns=['ID'], inplace=True)
    # joined_df.drop(columns=['unique_key', 'temp_group_id'], inplace=True)

    # joined_df.drop(columns=['unique_key'], inplace=True)
    # Ensure the 'trip_id' column is at the start of the DataFrame
    cols = ['masa_id'] + [col for col in joined_df.columns if col != 'masa_id']
    joined_df = joined_df[cols]
    joined_df = joined_df.sort_values(by='masa_id')
    # Write the joined DataFrame to a new Excel file in the same directory, overriding if exists
    output_file = os.path.join(output_file_path, output_file_name_masof + '.xlsx')
    joined_df.to_excel(output_file, index=False)
    #     filtered_df.to_excel(output_file, index=False)
    for masa_id in joined_df['masa_id'].unique():
        # Create a folder for the current masa_id
        masa_id_folder_name = f'masa_id_{masa_id}'
        masa_id_folder = os.path.join(output_file_path, masa_id_folder_name)
        # Define the output file path
        file_name = f'masofim masa_id_{masa_id}.xlsx'
        output_file = os.path.join(masa_id_folder, file_name)
        if not os.path.exists(masa_id_folder):
            print(f"New directory: \nDirectory name:{masa_id_folder_name}")
            os.makedirs(masa_id_folder)
        else:
            print(f"the folder: {masa_id_folder_name} already exist")
        if not os.path.exists(output_file):
            print(f"New file: \nFile name: {file_name}\nFile path: {output_file}")
            # Filter the DataFrame for the current masa_id
            filtered_df = joined_df[joined_df['masa_id'] == masa_id]

            # Further filter the DataFrame to include only rows without "לא תקין"
            valid_rows = filtered_df[filtered_df.apply(
                lambda row: any(isinstance(val, str) and "לא תקין" in val for val in row if not pd.isna(val)), axis=1)]
            # Find the starting index of the first column that contains any of the keywords
            start_index = None
            for idx, col in enumerate(valid_rows.columns):
                if valid_rows[col].apply(
                        lambda val: isinstance(val, str) and any(keyword in val for keyword in keywords)).any():
                    start_index = idx
                    break

            if start_index is None:
                continue  # If no such column is found, move to the next masa_id
            # Find triplets of columns where the first column contains "לא תקין"
            columns_to_save = []
            # for i in range(start_index, len(valid_rows.columns), 3):
            #     triplet = valid_rows.columns[i:i + 3]
            #     if valid_rows[triplet[0]].apply(lambda val: isinstance(val, str) and "לא תקין" in val).any():
            #         columns_to_save.extend(triplet)
            i = start_index
            step_size = 3

            while i < len(valid_rows.columns):
                tripletx = valid_rows.columns[i]
                if tripletx == "נראות התחנה ממרחק":
                    x = 5
                # Alternate the step size between 3 and 2
                if tripletx == "אנא מלא לאחר הסיום טופס תחנה - רציף" or tripletx == "אנא מלא לאחר הסיום טופס שילוט משולב" or tripletx == "אנא מלא לאחר הסיום טופס שילוט שילוט טלוויזיוני רציף ולוז מרכזי" or tripletx == "אי/מדרכה" or tripletx =="סוג ספסל" or tripletx == "תאורה חיצונית" :
                    step_size =1
                elif  tripletx =="שפות" or tripletx == 'כפתור כריזה' or tripletx == 'יציאה או הגעה בזמן' or tripletx == 'תיקוף ביישומון' or tripletx == 'ביטחון אישי':
                    step_size = 2
                else:
                    step_size = 3

                # Move to the next set of columns
                if step_size == 2:
                    c = 45
                triplet = valid_rows.columns[i:i + step_size]
                i += step_size
                # Ensure the triplet is not empty and has the expected number of columns
                if len(triplet) > 0:
                    # if valid_rows[triplet[0]].apply(lambda val: isinstance(val, str) and "לא תקין" in val).any():
                    #     columns_to_save.extend(triplet)

                    for val in valid_rows[triplet[0]]:
                        if isinstance(val, str):
                            if "לא תקין" in val:
                                columns_to_save.extend(triplet)
                                break

            additional_columns = valid_rows.iloc[:, :start_index]
            # Get the column names up to the start index
            additional_columns = additional_columns.columns.tolist()
            for col in reversed(additional_columns):
                columns_to_save.insert(0, col)
            # Remove duplicates while preserving order
            columns_to_save = list(dict.fromkeys(columns_to_save))

            # Filter the DataFrame to keep only the necessary columns
            valid_rows = valid_rows[columns_to_save]

            # Remove columns that are empty across all rows
            valid_rows = valid_rows.dropna(axis=1, how='all')
            # Save the valid filtered DataFrame to an Excel file
            valid_rows.to_excel(output_file, index=False)
        else:
            print(f"the file: {filename} already exist")
    print("Join of specified Excel files has been saved to:", output_file)
if dfs_nesia:
    joined_df = pd.concat(dfs_nesia, axis=0, ignore_index=True)
    if 'שם תחנת עלייה' not in joined_df.columns:
        joined_df.insert(joined_df.columns.get_loc('מקט תחנת עלייה') + 1, 'שם תחנת עלייה',joined_df['מקט תחנת עלייה'].apply(lambda x: stationNameByMakat(x)))
    # Order by Date and Time
    joined_df['שעת התחלה'] = pd.to_datetime(joined_df['שעת התחלה'])
    joined_df = joined_df.sort_values(by='שעת התחלה')
    # Write the joined DataFrame to a new Excel file in the same directory, overriding if exists
    # Create a unique key by combining 'שם' and the date part of 'שעת התחלה'
    joined_df['unique_key'] = joined_df['שם'] + '_' + joined_df['שעת התחלה'].dt.date.astype(str)

    # Generate a 'trip_id' for each unique key
    joined_df['temp_group_id'] = joined_df.groupby('unique_key').ngroup() + 1
    masa_ids = []

    # joined_df['masa_id'] = joined_df.groupby('unique_key').ngroup() + 1
    # Iterate over each row in the DataFrame
    for index, row in joined_df.iterrows():
        # print(row)
        # Check the condition and process the 'שם' column accordingly
        if 'שם' in joined_df.columns:
            name_processed = row['שם'][:-12] if row['שם'].endswith('Barshai LTD') else row['שם']
        elif 'Name' in joined_df.columns:
            name_processed = row['Name'][:-12] if row['Name'].endswith('Barshai LTD') else row['Name']
        print(row['סוג בדיקה'], name_processed, row['שעת התחלה'])
        print(row['שעת התחלה'] == pd.to_datetime('04/06/2024  17:38:53'))
        if (row['שעת התחלה'] == pd.to_datetime('04/06/2024  17:38:53')):
            y = 6
        # if name_processed=='Ram Asaad':
        #     c=8
        # Call the makatByDateAndName function with the processed name and 'שעת התחלה'
        if 'שעת התחלה' in joined_df.columns:
            masa_id = makatByDateAndName(row['שעת התחלה'], name_processed)
        elif 'Start time' in joined_df.columns:
            masa_id = makatByDateAndName(row['Start time'], name_processed)
        # Append the result to the masa_ids list
        masa_ids.append(masa_id)

    # Assign the list of results to a new column in the DataFrame
    joined_df['masa_id'] = masa_ids
    # Drop the temporary 'unique_key' column
    joined_df.drop(columns=['ID'], inplace=True)
    joined_df.drop(columns=['unique_key', 'temp_group_id'], inplace=True)

    # joined_df.drop(columns=['unique_key'], inplace=True)
    # Ensure the 'trip_id' column is at the start of the DataFrame
    cols = ['masa_id'] + [col for col in joined_df.columns if col != 'masa_id']
    joined_df = joined_df[cols]
    joined_df = joined_df.sort_values(by='masa_id')

    output_file = os.path.join(output_file_path, output_file_name_nesia + '.xlsx')
    joined_df.to_excel(output_file, index=False)

    # # Iterate through each unique masa_id
    # for masa_id in joined_df['masa_id'].unique():
    #     # Filter the DataFrame for the current masa_id
    #     filtered_df = joined_df[joined_df['masa_id'] == masa_id]
    #
    #     # Further filter the DataFrame to include only rows without "לא תקין"
    #     valid_rows = filtered_df[~filtered_df.apply(
    #         lambda row: any(isinstance(val, str) and "לא תקין" in val for val in row if not pd.isna(val)), axis=1)]
    #
    #     # Create a folder for the current masa_id
    #     masa_id_folder = os.path.join(output_file_path, f'masa_id_{masa_id}')
    #     if not os.path.exists(masa_id_folder):
    #         os.makedirs(masa_id_folder)
    #
    #     # Define the output file path
    #     output_file = os.path.join(masa_id_folder, f'masa_id_{masa_id}.xlsx')
    #
    #     # Save the valid filtered DataFrame to an Excel file
    #     valid_rows.to_excel(output_file, index=False)
    # Iterate through each unique masa_id
    # for masa_id in joined_df['masa_id'].unique():
    #     # Filter the DataFrame for the current masa_id
    #     filtered_df = joined_df[joined_df['masa_id'] == masa_id]
    #
    #     # Create a folder for the current masa_id
    #     masa_id_folder = os.path.join(output_file_path, f'masa_id_{masa_id}')
    #     if not os.path.exists(masa_id_folder):
    #         os.makedirs(masa_id_folder)
    #
    #     # Define the output file path
    #     output_file = os.path.join(masa_id_folder, f'nesiaot masa_id_{masa_id}.xlsx')
    #
    #     # Save the filtered DataFrame to an Excel file
    #     filtered_df.to_excel(output_file, index=False)
    #     filtered_df.to_excel(output_file, index=False)
    for masa_id in joined_df['masa_id'].unique():
        # Create a folder for the current masa_id
        masa_id_folder_name = f'masa_id_{masa_id}'
        masa_id_folder = os.path.join(output_file_path, masa_id_folder_name)
        # Define the output file path
        file_name = f'nesiot masa_id_{masa_id}.xlsx'
        output_file = os.path.join(masa_id_folder, file_name)
        if not os.path.exists(masa_id_folder):
            print(f"New directory: \nDirectory name:{masa_id_folder_name}")
            os.makedirs(masa_id_folder)
        else:
            print(f"the folder: {masa_id_folder_name} already exist")
        if not os.path.exists(output_file):
            print(f"New file: \nFile name: {file_name}\nFile path: {output_file}")
            # Filter the DataFrame for the current masa_id
            filtered_df = joined_df[joined_df['masa_id'] == masa_id]

            # Further filter the DataFrame to include only rows without "לא תקין"
            valid_rows = filtered_df[filtered_df.apply(
                lambda row: any(isinstance(val, str) and "לא תקין" in val for val in row if not pd.isna(val)), axis=1)]
            # Find the starting index of the first column that contains any of the keywords
            start_index = None
            for idx, col in enumerate(valid_rows.columns):
                if valid_rows[col].apply(
                        lambda val: isinstance(val, str) and any(keyword in val for keyword in keywords)).any():
                    start_index = idx
                    break

            if start_index is None:
                continue  # If no such column is found, move to the next masa_id
            # Find triplets of columns where the first column contains "לא תקין"
            columns_to_save = []
            # for i in range(start_index, len(valid_rows.columns), 3):
            #     triplet = valid_rows.columns[i:i + 3]
            #     if valid_rows[triplet[0]].apply(lambda val: isinstance(val, str) and "לא תקין" in val).any():
            #         columns_to_save.extend(triplet)
            i = start_index
            step_size = 3

            while i < len(valid_rows.columns):
                tripletx = valid_rows.columns[i]
                if tripletx == "כפתור כריזה":
                    x = 5
                # Alternate the step size between 3 and 2
                if tripletx.strip() == "שפות" or tripletx.strip() == 'כריזה' or tripletx.strip() == 'יציאה או הגעה בזמן' or tripletx.strip() == 'תיקוף ביישומון' or tripletx.strip() == 'ביטחון אישי':
                    step_size = 2
                else:
                    step_size = 3

                # Move to the next set of columns
                if step_size == 2:
                    c = 45
                triplet = valid_rows.columns[i:i + step_size]
                i += step_size
                # Ensure the triplet is not empty and has the expected number of columns
                if len(triplet) > 0:
                    # if valid_rows[triplet[0]].apply(lambda val: isinstance(val, str) and "לא תקין" in val).any():
                    #     columns_to_save.extend(triplet)

                    for val in valid_rows[triplet[0]]:
                        if isinstance(val, str):
                            if "לא תקין" in val:
                                columns_to_save.extend(triplet)
                                break

            additional_columns = valid_rows.iloc[:, :start_index]
            # Get the column names up to the start index
            additional_columns = additional_columns.columns.tolist()
            for col in reversed(additional_columns):
                columns_to_save.insert(0, col)
            # Remove duplicates while preserving order
            columns_to_save = list(dict.fromkeys(columns_to_save))

            # Filter the DataFrame to keep only the necessary columns
            valid_rows = valid_rows[columns_to_save]

            # Remove columns that are empty across all rows
            valid_rows = valid_rows.dropna(axis=1, how='all')
            # Save the valid filtered DataFrame to an Excel file
            valid_rows.to_excel(output_file, index=False)
        else:
            print(f"the file: {filename} already exist")
    print("Join of specified Excel files has been saved to:", output_file)
else:
    print("No Excel files to join.")
  # Iterate through each unique masa_id

######################################
# import os
# from openpyxl import load_workbook
# import pandas as pd
#
# # Define the directory containing Excel files
# directory = r'C:\Users\AvichayKadosh\OneDrive - ברשאי\ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\חווית לקוח\02 - פורמטים לבדיקה\טפסי בדיקה חווית לקוח'
#
# # Initialize an empty list to store the DataFrames
# dfs = []
#
# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".xlsx") and filename != 'סיכום.xlsx':  # Skip the output file
#         # Read each Excel file into a DataFrame
#         file_path = os.path.join(directory, filename)
#         df = pd.read_excel(file_path, index_col=None)
#
#         # Drop the ID column
#         # df = df.drop(columns=['ID'])
#
#         # Append the DataFrame to the list
#         dfs.append(df)
#
# # Perform join operation if there are files to join
# if dfs:
#     # Join DataFrames
#     joined_df = pd.concat(dfs, axis=0, ignore_index=True)
#
#     # Write the joined DataFrame to a new Excel file in the same directory, overriding if exists
#     output_file = os.path.join(directory, 'סיכום.xlsx')
#     joined_df.to_excel(output_file, index=False)
#
#     print("Join of all Excel files has been saved to:", output_file)
# else:
#     print("No Excel files to join.")
#############################################################################
# import os
# import pandas as pd
#
# # Define the directory containing Excel files
# directory = r'C:\Users\AvichayKadosh\OneDrive - ברשאי\ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\חווית לקוח\02 - פורמטים לבדיקה\טפסי בדיקה חווית לקוח\טפסים בלי פורמטים'
#
# # Initialize an empty list to store DataFrames
# dfs = []
#
# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".xlsx") and filename != 'סיכום.xlsx':  # Skip the output file
#         # Read each Excel file into a DataFrame and append to the list
#         file_path = os.path.join(directory, filename)
#         df = pd.read_excel(file_path)
#         dfs.append(df)
#
# # Perform join operation if there are files to join
# if dfs:
#     # Join DataFrames
#     joined_df = pd.concat(dfs, axis=0, ignore_index=True)
#
#     # Write the joined DataFrame to a new Excel file in the same directory, overriding if exists
#     output_file = os.path.join(directory, 'סיכום.xlsx')
#     joined_df.to_excel(output_file, index=False)
#
#     print("Join of all Excel files has been saved to:", output_file)
# else:
#     print("No Excel files to join.")