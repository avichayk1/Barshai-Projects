import os
import pandas as pd
import streamlit as st
import time


def load_file_in_chunks(uploaded_file, chunk_size=1500000, sleep_duration=1):
    # Initialize an empty list to store the chunks
    chunks = []

    # Read the file in chunks
    for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size):
        chunks.append(chunk)
        time.sleep(sleep_duration)  # Add a sleep duration between processing chunks

    # Combine all chunks into a single DataFrame
    file_content = pd.concat(chunks, ignore_index=True)

    return file_content


def get_columns_from_txt(file_content):
    first_line = file_content.readline().strip()
    return first_line.split(',')  # Return columns


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

    uploaded_files = st.file_uploader("Upload TXT files", accept_multiple_files=True, type="txt")

    # Dictionary to store file name and its content as a pair
    if "file_data" not in st.session_state:
        st.session_state["file_data"] = {}

    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    st.title("GTFS Merge and Plot Tool")

    # Reset button
    if st.button("Reset All"):
        reset_session_state()
        st.rerun()  # Rerun the app to reflect the reset

    # Initial merge setup
    st.header("Merge Files")
    if "merged_data" not in st.session_state:
        st.session_state["merged_data"] = None

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    # Extract just the file names from the dictionary (keys of file_data)
    file_names = [file.name for file in uploaded_files]  # Use uploaded_files instead of session state

    # File selection
    selected_file = st.selectbox("Select a file to merge:", file_names)
    if selected_file:
        uploaded_file = next((file for file in uploaded_files if file.name == selected_file), None)

        if uploaded_file.name not in st.session_state["file_data"]:
            # Load file content in chunks and concatenate them
            file_content = load_file_in_chunks(uploaded_file)

            # Store the loaded data in session state
            st.session_state["file_data"][uploaded_file.name] = file_content
            st.success(f"File '{uploaded_file.name}' successfully loaded in chunks.")
        else:
            # Get the file content for the selected file
            file_content = st.session_state["file_data"][selected_file]

        columns = file_content.columns.tolist()  # Use the DataFrame columns
        selected_columns = st.multiselect("Select columns to include from the file:", columns, default=columns)

        if st.session_state["merged_data"] is not None:
            join_column = st.selectbox("Select the column to join on:", st.session_state["merged_data"].columns)
        else:
            join_column = None

        if st.button("Add File to Merge"):
            if selected_file in st.session_state["uploaded_files"]:
                st.warning(f"File '{selected_file}' has already been added.")
                return

            # If merged_data exists, merge with the new file
            if st.session_state["merged_data"] is None:
                # First file: initialize merged_data when it's the first upload after reset
                st.session_state["merged_data"] = file_content
                st.success(f"File '{selected_file}' loaded as the base for merging.")
            else:
                # If merged_data exists, merge with the new file
                if join_column is None:
                    st.error("You must select a column to join on.")
                    return

                try:
                    st.session_state["merged_data"] = pd.merge(
                        st.session_state["merged_data"], file_content, on=join_column
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

        st.sidebar.header("Active Filters")
        if st.session_state["filters"]:
            for idx, f in enumerate(st.session_state["filters"], start=1):
                st.sidebar.write(f"{idx}. {f['column']} {f['comparison']} '{f['value']}'")
        else:
            st.sidebar.text("No active filters")

    # Apply filters to merged data
    if st.session_state["merged_data"] is not None:
        filtered_data = apply_filters(st.session_state["merged_data"])
        st.session_state["merged_data"] = filtered_data
        limited_data = filtered_data.head(200)
        st.dataframe(limited_data)


if __name__ == "__main__":
    main()
