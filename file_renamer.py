import os

import pandas as pd
import streamlit as st


def replace_words(folder_path, old, new):
    # Check if the folder path is valid
    if not os.path.exists(folder_path):
        st.write(f"The folder path '{folder_path}' does not exist!")
        return

    # Get the list of files in the folder
    file_list = os.listdir(folder_path)

    # Replace the old word with the new word in each filename
    results = []
    for old_file_name in file_list:
        old_file_path = os.path.join(folder_path, old_file_name)
        # Skip directories
        if os.path.isdir(old_file_path):
            continue
        new_file_name = old_file_name.replace(old, new)
        if new_file_name != old_file_name:
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(old_file_path, new_file_path)
            results.append([old_file_name, new_file_name])

    return results


def add_prefix(folder_path, prefix):
    # Check if the folder path is valid
    if not os.path.exists(folder_path):
        st.write(f"The folder path '{folder_path}' does not exist!")
        return

    # Check if the prefix is valid
    if not prefix:
        st.write("Please enter a prefix!")
        return

    # Get the list of files in the folder
    file_list = os.listdir(folder_path)

    # Add the prefix to the filename
    results = []
    for old_file_name in file_list:
        old_file_path = os.path.join(folder_path, old_file_name)
        # Skip directories
        if os.path.isdir(old_file_path):
            continue
        file_name, file_ext = os.path.splitext(old_file_name)
        new_file_name = prefix + file_name + file_ext
        new_file_path = os.path.join(folder_path, new_file_name)
        results.append([old_file_name, new_file_name])

    # Rename the files
    for old_file_name, new_file_name in results:
        old_file_path = os.path.join(folder_path, old_file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(old_file_path, new_file_path)

    return results


# Define a dictionary of functions
functions = {
    "Replace Words": replace_words,
    "Add Prefix": add_prefix,
}

# Define the Streamlit app
def app():
    # Define the UI elements
    st.title("Rename files in folder")
    folder_path = st.text_input("Enter a folder path:")

    # Check if the folder path is empty
    if not folder_path:
        st.write("Please enter a folder path!")
        return

    # Check if the folder path is valid
    if not os.path.exists(folder_path):
        st.write(f"The folder path '{folder_path}' does not exist!")
        return

    file_list = os.listdir(folder_path)
    st.dataframe(file_list)

    function_name = st.selectbox("Select a function:", list(functions.keys()))
    if function_name == "Add Prefix":
        prefix = st.text_input("Enter a prefix:")
        function = functions[function_name]

        # Show a preview of the filename changes
        file_list = os.listdir(folder_path)
        preview = []
        for old_file_name in file_list:
            old_file_path = os.path.join(folder_path, old_file_name)
            # Skip directories
            if os.path.isdir(old_file_path):
                continue
            file_name, file_ext = os.path.splitext(old_file_name)
            new_file_name = prefix + file_name + file_ext
            preview.append([old_file_name, new_file_name])
        st.write(pd.DataFrame(preview, columns=["Old Filename", "New Filename"]))

        if st.button("Execute"):
            results = function(folder_path, prefix)
            st.write(pd.DataFrame(results, columns=["Old Filename", "New Filename"]))

            # Get the updated list of files in the folder
            file_list = os.listdir(folder_path)

    if function_name == "Replace Words":
        old = st.text_input("Enter the word to replace:", value="")
        new = st.text_input("Enter the new word:", value="")
        function = functions[function_name]

        # Show a preview of the filename changes
        file_list = os.listdir(folder_path)
        preview = []
        for old_file_name in file_list:
            old_file_path = os.path.join(folder_path, old_file_name)
            # Skip directories
            if os.path.isdir(old_file_path):
                continue
            new_file_name = old_file_name.replace(old, new)
            preview.append([old_file_name, new_file_name])
        st.write(pd.DataFrame(preview, columns=["Old Filename", "New Filename"]))

        if st.button("Execute"):
            results = function(folder_path, old, new)
            st.write(pd.DataFrame(results, columns=["Old Filename", "New Filename"]))


# Run the app
if __name__ == "__main__":
    app()
