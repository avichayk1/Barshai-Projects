import pandas as pd
import os
from tkinter import Tk, Label, Entry, Button, Listbox, filedialog, StringVar, END, MULTIPLE


def select_folder(var):
    """Open a folder dialog and set the chosen folder path."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        var.set(folder_path)


def load_files():
    """Load file names from the selected folder and display only the file names in the listbox."""
    try:
        folder_path = input_path.get()
        if not os.path.exists(folder_path):
            print("Invalid folder path")
            return

        all_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]  # Filter for .txt files
        files_listbox.delete(0, END)
        for file in all_files:
            # Insert only the file name into the listbox (not the full path)
            files_listbox.insert(END, file)

    except Exception as e:
        print(f"Error loading files: {e}")


def show_columns():
    """Show columns of the selected file in the columns listbox."""
    try:
        # Get the selected file name (not the full path)
        selected_file_name = files_listbox.get(files_listbox.curselection())
        folder_path = input_path.get()
        selected_file = os.path.join(folder_path, selected_file_name)  # Get full path

        # Read the selected file
        df = pd.read_csv(selected_file, delimiter='\t', encoding='utf-8')
        # Insert columns into the listbox (one column per row)
        for col in df.columns:
            # Split the column by commas if applicable and insert into listbox
            split_columns = col.split(',')  # Split by commas
            for split_col in split_columns:
                columns_listbox.insert(END, split_col)  # Insert each split column separately


    except Exception as e:
        print(f"Error showing columns: {e}")


def add_file_selection():
    """Add selected file, columns, and join column details to the merge process."""
    try:
        # Get selected file name and its full path
        selected_file_name = files_listbox.get(files_listbox.curselection())
        folder_path = input_path.get()
        selected_file = os.path.join(folder_path, selected_file_name)

        selected_columns = [columns_listbox.get(i) for i in columns_listbox.curselection()]
        join_column = join_column_entry.get()

        # Add the file selection with full path to the selected files list
        selected_files.append((selected_file, selected_columns, join_column))

        # Split the details into separate lines for easier reading
        file_details = f"File: {selected_file_name}\nColumns: {', '.join(selected_columns)}\nJoin On: {join_column}\n"

        # Insert the file details on new lines
        selected_files_listbox.insert(END, file_details)

    except Exception as e:
        print(f"Error adding file selection: {e}")


def process_files():
    """Merge files based on user input."""
    output = output_path.get()
    if not selected_files or not output:
        print("Please select files and specify an output folder.")
        return

    try:
        # Start merging with the first file
        file_path, include_columns, _ = selected_files[0]
        merged_df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
        if include_columns:
            merged_df = merged_df[include_columns]

        # Merge remaining files
        for i in range(1, len(selected_files)):
            file_path, include_columns, join_column = selected_files[i]
            next_df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
            if include_columns:
                next_df = next_df[include_columns]
            merged_df = pd.merge(merged_df, next_df, on=join_column)

        # Save the output
        output_file = f"{output}/merged_output.txt"
        merged_df.to_csv(output_file, sep='\t', index=False, encoding="utf-8")
        print(f"Files successfully merged and saved to {output_file}")
    except Exception as e:
        print(f"Error processing files: {e}")


# Initialize GUI
root = Tk()
root.title("Dynamic TXT Merge Tool")

# Input Folder
Label(root, text="Input Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_path = StringVar()
Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=5, pady=5)
Button(root, text="Browse", command=lambda: select_folder(input_path)).grid(row=0, column=2, padx=5, pady=5)

# Output Folder
Label(root, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_path = StringVar()
Entry(root, textvariable=output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
Button(root, text="Browse", command=lambda: select_folder(output_path)).grid(row=1, column=2, padx=5, pady=5)

# Files Listbox (Allow multiple selections for merging)
Label(root, text="Select Files to Merge:").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
files_listbox = Listbox(root, selectmode=MULTIPLE, width=50, height=10)
files_listbox.grid(row=2, column=1, padx=5, pady=5)
Button(root, text="Load Files", command=load_files).grid(row=2, column=2, padx=5, pady=5)

# Show Columns
Button(root, text="Show Columns", command=show_columns).grid(row=3, column=2, padx=5, pady=5)
columns_listbox = Listbox(root, selectmode=MULTIPLE, width=50, height=10)
columns_listbox.grid(row=3, column=1, padx=5, pady=5)

# File Selection Details
Label(root, text="Join On Column:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
join_column_entry = Entry(root, width=50)
join_column_entry.grid(row=4, column=1, padx=5, pady=5)

Button(root, text="Add File", command=add_file_selection).grid(row=5, column=1, padx=5, pady=5)

# Selected Files Listbox
Label(root, text="Selected Files and Details:").grid(row=6, column=0, padx=5, pady=5, sticky="ne")
selected_files_listbox = Listbox(root, width=70, height=10)
selected_files_listbox.grid(row=6, column=1, padx=5, pady=5)

# Merge Button
Button(root, text="Merge Files", command=process_files).grid(row=7, column=1, padx=5, pady=10)

# Variables
selected_files = []

# Run the GUI
root.mainloop()
