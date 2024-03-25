import csv
import shutil
import os


def move_files(csv_file_path, destination_folder, file_path_column_name):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        if file_path_column_name not in csv_reader.fieldnames:
            print(f"Column '{file_path_column_name}' not found.")
            return

        for row in csv_reader:
            file_path = row[file_path_column_name]

            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                destination_path = os.path.join(destination_folder, filename)
                shutil.move(file_path, destination_path)
                print(f"Moved {file_path} to {destination_path}")
            else:
                print(f"File {file_path} not found.")


csv_file_path = 'files.csv'
destination_folder = 'destination_folder'
file_path_column_name = 'file_path_column'
move_files(csv_file_path, destination_folder, file_path_column_name)
