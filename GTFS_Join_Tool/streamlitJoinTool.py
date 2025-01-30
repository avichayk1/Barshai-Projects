import os
import pandas as pd
import streamlit as st
import time


def reset_session_state():
    st.session_state["merged_data"] = None
    st.session_state["uploaded_files"] = []
    st.session_state["file_data"] = {}
    st.session_state["filters"] = []


def apply_filters(data):
    original_types = data.dtypes
    for filter_criteria in st.session_state["filters"]:
        column = filter_criteria['column']
        value = filter_criteria['value']
        comparison = filter_criteria['comparison']
        data[column] = data[column].astype(str)
        if comparison == "Match":
            data = data[data[column] == value]
        elif comparison == "Does Not Match":
            data = data[data[column] != value]
    for column, dtype in original_types.items():
        data[column] = data[column].astype(dtype)
    return data


def main():
    st.set_page_config(layout="wide")
    st.title("GTFS Merge and Plot Tool")

    if "file_data" not in st.session_state:
        st.session_state["file_data"] = {}
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []
    if "merged_data" not in st.session_state:
        st.session_state["merged_data"] = None
    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    uploaded_files = st.file_uploader("Upload TXT files", accept_multiple_files=True, type="txt")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state["file_data"]:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    time.sleep(1)  # הדמיית זמן טעינה
                    try:
                        file_content = pd.read_csv(uploaded_file)
                        st.session_state["file_data"][uploaded_file.name] = file_content
                        st.session_state["uploaded_files"].append(uploaded_file.name)
                        st.success(f"{uploaded_file.name} uploaded successfully!")
                    except Exception as e:
                        st.error(f"Error reading {uploaded_file.name}: {e}")

    st.sidebar.header("Uploaded Files")
    for file in st.session_state["uploaded_files"]:
        st.sidebar.text(file)

    st.header("Merge Files")
    file_names = list(st.session_state["file_data"].keys())
    selected_file = st.selectbox("Select a file to merge:", file_names)
    if selected_file:
        file_content = st.session_state["file_data"][selected_file]
        columns = file_content.columns.tolist()
        selected_columns = st.multiselect("Select columns to include:", columns, default=columns)
        if st.session_state["merged_data"] is not None:
            join_column = st.selectbox("Select column to join on:", st.session_state["merged_data"].columns)
        else:
            join_column = None

        if st.button("Add File to Merge"):
            if selected_file in st.session_state["uploaded_files"]:
                st.warning(f"File '{selected_file}' has already been added.")
                return
            if st.session_state["merged_data"] is None:
                st.session_state["merged_data"] = file_content[selected_columns]
                st.success(f"{selected_file} set as the base for merging.")
            else:
                if join_column is None:
                    st.error("You must select a column to join on.")
                    return
                try:
                    st.session_state["merged_data"] = pd.merge(
                        st.session_state["merged_data"], file_content[selected_columns], on=join_column
                    )
                    st.success(f"{selected_file} successfully merged.")
                except Exception as e:
                    st.error(f"Error merging: {e}")
                    return
            st.session_state["uploaded_files"].append(selected_file)

    st.sidebar.header("Merged Files")
    for file in st.session_state["uploaded_files"]:
        st.sidebar.text(file)

    st.header("Filters")
    if st.session_state["merged_data"] is not None:
        filter_column = st.selectbox("Choose a column to filter:", st.session_state["merged_data"].columns)
        filter_value = st.text_input(f"Enter value for filtering '{filter_column}':")
        comparison = st.radio("Filter Type:", ["Match", "Does Not Match"])
        if st.button("Apply Filter"):
            if filter_value.strip():
                st.session_state["filters"].append({
                    'column': filter_column,
                    'value': filter_value,
                    'comparison': comparison
                })
                st.success(f"Filter applied: {filter_column} {comparison} '{filter_value}'")
            else:
                st.warning("Please enter a valid filter value.")

    if st.session_state["merged_data"] is not None:
        filtered_data = apply_filters(st.session_state["merged_data"])
        st.session_state["merged_data"] = filtered_data
        st.dataframe(filtered_data.head(200))

    if st.button("Reset All"):
        reset_session_state()
        st.rerun()


if __name__ == "__main__":
    main()
