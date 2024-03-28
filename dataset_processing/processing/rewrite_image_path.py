import os
import csv


def extract_patient_id(file_path):
    start_index = file_path.find("Mass-Test_") + len("Mass-Test_")
    patient_id = file_path[start_index:start_index + 7]
    return patient_id


def find_pathology(patient_id, read_csv_path):
    with open(read_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row["patient_id"] == patient_id:
                return row["pathology"]

    # If patient_id is not found
    return None

def rewrite(root_folder, read_csv_path, write_csv_path):
    if not os.path.exists(root_folder):
        print("Root folder not found.")
        return

    image_paths = {}
    cropped_paths = {}
    masked_paths = {}
    patient_ids_seen = set()  # To keep track of seen patient IDs
    file_paths_seen = set()   # To keep track of seen file paths

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.dcm'):
                file_path = os.path.join(root, file)
                if 'Mass-Test' in file_path:
                    if '_1' in file_path:
                        if '1-1.dcm' in file:
                            masked_paths[file_path] = file_path
                        elif '1-2.dcm' in file:
                            cropped_paths[file_path] = file_path
                    else:
                        patient_id = extract_patient_id(file_path)
                        if patient_id not in patient_ids_seen and file_path not in file_paths_seen:
                            image_paths[file_path] = file_path
                            patient_ids_seen.add(patient_id)
                            file_paths_seen.add(file_path)

    with open(write_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["patient_id", "image_path", "cropped_path", "masked_path", "pathology"])  # Add pathology header
        for image_path, cropped_path, masked_path in zip(image_paths.values(), cropped_paths.values(),
                                                         masked_paths.values()):
            patient_id = extract_patient_id(image_path)  # Extract patient ID
            print(patient_id)
            pathology = find_pathology(patient_id, read_csv_path)  # Find pathology based on patient ID
            print(pathology)
            writer.writerow([patient_id, image_path, cropped_path, masked_path, pathology])

    print("New CSV file created successfully.")



root_folder = "D:/Project/dataset_processing/CBIS-DDSM"
write_csv_path = "data_result.csv"
read_csv_path = "mass_case_description_test_set_mini.csv"
rewrite(root_folder,read_csv_path, write_csv_path)
