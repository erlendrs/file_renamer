import os
import streamlit as st
import pandas as pd

def rename_files(file_mapping, folder):
    # create a dictionary of old and new filenames
    name_map = dict(zip(file_mapping['Old Name'], file_mapping['New Name']))

    # get the list of files in the folder
    files = os.listdir(folder)

    # match the filenames to the files in the folder
    for old_name, new_name in name_map.items():
        if old_name is None or new_name is None:
            continue
        if new_name in files:
            st.write(f'Warning: {new_name} already exists and will be overwritten.')

    confirm = st.button("Rename Files")
    if confirm:
        st.write("Renaming files...")
        for old_name, new_name in name_map.items():
            if old_name is None or new_name is None:
                continue
            if new_name in files:
                os.rename(os.path.join(folder, new_name), os.path.join(folder, f'{new_name}.old'))
            os.rename(os.path.join(folder, old_name), os.path.join(folder, new_name))
        st.write("Files renamed.")

# define the Streamlit app
def app():
    st.title("File Renamer")

    # define the input parameters
    folder = st.text_input("Folder", value='./my_folder')

    # get the list of files in the folder
    files = os.listdir(folder)

    # preview the files in the folder
    st.write("Files in folder:")
    st.write(files)

    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        file_mapping = pd.read_csv(uploaded_file, header=None)
        file_mapping.columns = ['New Name']
        file_mapping['Number'] = file_mapping['New Name'].str.extract(r'(\d+)', expand=False)
        matching_files = []
        for old_name in files:
            for number in file_mapping['Number']:
                if number in old_name:
                    matching_files.append(old_name)
                    break
        matching_df = pd.DataFrame({'Old Name': matching_files})
        matching_df['Number'] = matching_df['Old Name'].str.extract(r'(\d+)', expand=False)
        file_mapping = file_mapping.merge(matching_df, on='Number', how='inner')
        preview_df = file_mapping[['Old Name', 'New Name']].copy()
        preview_df.rename(columns={'Old Name': 'Current Filename', 'New Name': 'New Filename'}, inplace=True)
        st.write("Preview of matching filenames:")
        st.write(preview_df)
        rename_files(file_mapping, folder)

# run the Streamlit app
if __name__ == '__main__':
    app()
