# Join Tool

This tool is designed for merging and plotting data from multiple `.txt` files. The user can upload files, select columns to include, merge them based on a common column, and visualize the data through plots.

<img src="GTFS Merge and Plot Tool.png" alt="Description" width="600"/>

## Features
- **File Merge**: Merge multiple `.txt` files by selecting columns and choosing a common column for merging.
- **Data Preview**: Preview the merged data up to the first 200 rows.
- **Save Merged Data**: Save the merged data as a CSV file.
- **Plotting**: Generate line plots from numeric data columns.

## Running the Application with `start.bat`

To make it easier to run the application, you can use the `start.bat` file. If you save both the `streamlitJoinTool.py` and `start.bat` files in the same folder, you can simply run the `.bat` file to launch the app.


## Requirements
- Python 3.x
- Streamlit
- Pandas

You can install the required dependencies using `pip`:

```bash
pip install streamlit pandas
```

## Usage

1. **Run the application:**
    After installing the dependencies, run the following command to start the Streamlit app:

    ```bash
    streamlit run streamlitJoinTool.py
2. **Input Folder:**

    + Enter the path to the folder containing the .txt files you want to merge.
    + If the folder exists and contains .txt files, the application will display a list of files to choose from.
3. **Select Files to Merge:**
   + Choose a file from the list and select which columns to include in the merge.
   + If you are merging with another file, select a common column to join on.
4. **Merged Data:**
    + Once files are merged, the first 200 rows of the merged data will be displayed.
    + You can enter a path to save the merged data as a CSV file.
5. **Plot Data:**
    + If the merged data contains numeric columns, you can select columns to plot.
    Generate a line plot based on the selected columns.
6. **Reset:**
   + Press the "Reset All" button to reset the session, clear all data, and start fresh.
## Functions

- **`get_columns_from_txt(file_path)`**  
  Reads the first line of a `.txt` file and splits it into columns.

- **`load_txt_files(folder)`**  
  Loads all `.txt` files from a specified folder.

- **`reset_session_state()`**  
  Resets the session state, clearing the merged data, uploaded files, and input folder.

- **`main()`**  
  The main function that runs the Streamlit app, handling file uploads, merging, saving, and plotting.
