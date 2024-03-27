import os
import shutil

def move_files(file_path, destination_folder, folder_name):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        folder_path = os.path.join(destination_folder, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        destination_path = os.path.join(folder_path, filename)
        shutil.move(file_path, destination_path)
        print(f"Moved {file_path} to {destination_path}")
    else:
        print(f"File {file_path} not found.")

