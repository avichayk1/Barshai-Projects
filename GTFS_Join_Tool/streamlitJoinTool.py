import os
import pandas as pd
import streamlit as st


def get_columns_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        first_line = f.readline().strip()
        return first_line.split(',')


def load_txt_files(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    return files


def reset_session_state():
    # Reset session state variables
    st.session_state["merged_data"] = None
    st.session_state["uploaded_files"] = []
    st.session_state["input_folder"] = ""  # Reset the input folder path
    st.session_state["filters"] = []  # Reset filters


def apply_filters(data):
    original_types = data.dtypes

    # Apply all filters stored in session state
    for filter_criteria in st.session_state["filters"]:
        column = filter_criteria['column']
        value = filter_criteria['value']
        comparison = filter_criteria['comparison']

        # Convert column to string for consistency
        data[column] = data[column].astype(str)

        # Apply filter based on comparison
        if comparison == "Match":
            data = data[data[column] == value]
        elif comparison == "Does Not Match":
            data = data[data[column] != value]
    for column, dtype in original_types.items():
        data[column] = data[column].astype(dtype)
    return data


def main():
    st.set_page_config(layout="wide")
    # Initialize 'filters' key if it doesn't exist
    if "filters" not in st.session_state:
        st.session_state["filters"] = []
    st.title("GTFS Merge and Plot Tool")

    # Reset button
    if st.button("Reset All"):
        reset_session_state()
        st.rerun()  # Rerun the app to reflect the reset

    # Input folder
    if "input_folder" not in st.session_state:
        st.session_state["input_folder"] = ""  # Initialize the session state for input folder

    input_folder = st.text_input("Enter the input folder path:", value=st.session_state["input_folder"])
    st.session_state["input_folder"] = input_folder

    # Only check if the folder exists if it's not an empty string
    if input_folder and not os.path.exists(input_folder):
        st.error("The specified folder does not exist.")
        return

    # Only load txt files if the folder exists
    if input_folder and os.path.exists(input_folder):
        txt_files = load_txt_files(input_folder)
        if not txt_files:
            st.error("No TXT files found in the specified folder.")
            return
    else:
        txt_files = []  # If folder is empty or not set, leave txt_files empty

    # Initial merge setup
    st.header("Merge Files")
    if "merged_data" not in st.session_state:
        st.session_state["merged_data"] = None

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    # File selection
    selected_file = st.selectbox("Select a file to merge:", txt_files)
    if selected_file:
        file_path = os.path.join(input_folder, selected_file)
        columns = get_columns_from_txt(file_path)

        selected_columns = st.multiselect("Select columns to include from the file:", columns, default=columns)

        if st.session_state["merged_data"] is not None:
            join_column = st.selectbox("Select the column to join on:", st.session_state["merged_data"].columns)
        else:
            join_column = None

        if st.button("Add File to Merge"):
            if selected_file in st.session_state["uploaded_files"]:
                st.warning(f"File '{selected_file}' has already been added.")
                return

            data = pd.read_csv(file_path, usecols=selected_columns)

            if st.session_state["merged_data"] is None:
                # First file: initialize merged_data
                st.session_state["merged_data"] = data
                st.success(f"File '{selected_file}' loaded as the base for merging.")
            else:
                # If merged_data exists, merge with the new file
                if join_column is None:
                    st.error("You must select a column to join on.")
                    return

                try:
                    st.session_state["merged_data"] = pd.merge(
                        st.session_state["merged_data"], data, on=join_column
                    )
                    st.success(f"File '{selected_file}' successfully joined.")
                except Exception as e:
                    st.error(f"Error while merging: {e}")
                    return

            # Add the newly merged file to the list of uploaded files
            st.session_state["uploaded_files"].append(selected_file)

    # Sidebar: List of uploaded files
    st.sidebar.header("Files Already Merged")
    if st.session_state["uploaded_files"]:
        for file in st.session_state["uploaded_files"]:
            st.sidebar.text(file)
    else:
        st.sidebar.text("No files merged yet")
    # Filter setup
    st.header("Filters")
    if st.session_state["merged_data"] is not None:
        # Select column to filter
        filter_column = st.selectbox(
            "Choose a column to filter:",
            st.session_state["merged_data"].columns,
            help="Select a column to apply a filter."
        )

        # Input filter value
        filter_value = st.text_input(
            f"Enter a value for filtering '{filter_column}':",
            placeholder="Type a value to match..."
        )

        # Choose filter type
        comparison = st.radio(
            "Filter Type:",
            options=["Match", "Does Not Match"],
            help="Choose whether to include or exclude rows matching the value."
        )

        if st.button("Apply Filter"):
            if filter_value.strip():  # Ensure value is not empty
                st.session_state["filters"].append({
                    'column': filter_column,
                    'value': filter_value,
                    'comparison': comparison
                })
                st.success(f"Filter applied: {filter_column} = {filter_value}")
            else:
                st.warning("Please enter a valid value to filter.")
            # Display current filters
            # Sidebar: Active Filters
            st.sidebar.header("Active Filters")
            if st.session_state["filters"]:
                for idx, f in enumerate(st.session_state["filters"], start=1):
                    st.sidebar.write(f"{idx}. {f['column']} {f['comparison']} '{f['value']}'")
            else:
                st.sidebar.text("No active filters")
    # Apply filters to merged data
    if st.session_state["merged_data"] is not None:
        filtered_data = apply_filters(st.session_state["merged_data"])
        st.session_state["merged_data"]=filtered_data
        limited_data = filtered_data.head(200)
        st.dataframe(limited_data)

    # Enter the save path before pressing the save button
    if st.session_state["merged_data"] is not None:
        save_path = st.text_input("Enter the save path (with .csv extension):")
        if save_path and st.button("Save Merged Data"):
            st.session_state["merged_data"].to_csv(save_path, index=False)
            st.success(f"Merged data saved to {save_path}")


if __name__ == "__main__":
    main()
