import os
import pandas as pd
import streamlit as st


def get_columns_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # Use utf-8-sig to handle BOM
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


def main():
    st.title("Data Merge and Plot Tool")

    # Reset button
    if st.button("Reset All"):
        reset_session_state()
        st.rerun()  # Rerun the app to reflect the reset

    # Input folder
    if "input_folder" not in st.session_state:
        st.session_state["input_folder"] = ""  # Initialize the session state for input folder

    # Pass the value of the input folder from session state to the text input
    input_folder = st.text_input("Enter the input folder path:", value=st.session_state["input_folder"])

    # Update session state with the current input folder value
    st.session_state["input_folder"] = input_folder

    # Only show error if the input folder is not empty and doesn't exist
    if input_folder and not os.path.exists(input_folder):
        st.error("The specified folder does not exist.")
        return

    txt_files = load_txt_files(input_folder)
    if not txt_files:
        st.error("No TXT files found in the specified folder.")
        return

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

        selected_columns = st.multiselect(
            "Select columns to include from the file:", columns, default=columns
        )

        if st.session_state["merged_data"] is not None:
            # Display join column selection
            join_column = st.selectbox(
                "Select the column to join on:", st.session_state["merged_data"].columns
            )
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
                # Merge with existing data
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

    # Show merged data
    st.header("Merged Data")
    if st.session_state["merged_data"] is not None:
        # Limit to the first 200 rows
        limited_data = st.session_state["merged_data"].head(200)
        st.dataframe(limited_data)

    # Enter the save path before pressing the save button
    if st.session_state["merged_data"] is not None:
        save_path = st.text_input("Enter the save path (with .csv extension):")
        if save_path and st.button("Save Merged Data"):
            st.session_state["merged_data"].to_csv(save_path, index=False)
            st.success(f"Merged data saved to {save_path}")

    # Plotting options
    st.header("Plot Data")
    if st.session_state["merged_data"] is not None:
        numeric_columns = st.session_state["merged_data"].select_dtypes(include=['number']).columns
        if len(numeric_columns) == 0:
            st.warning("No numeric columns available for plotting.")
        else:
            x_axis = st.selectbox("Select X-axis column:", numeric_columns)
            y_axis = st.selectbox("Select Y-axis column:", numeric_columns)

            if st.button("Generate Plot"):
                st.line_chart(st.session_state["merged_data"][[x_axis, y_axis]])


if __name__ == "__main__":
    main()
