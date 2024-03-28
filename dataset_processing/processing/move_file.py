import os
import csv
import shutil

def move_files(csv_file_path, root_folder):
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    malignant_folder = os.path.join(root_folder, "malignant")
    benign_folder = os.path.join(root_folder, "benign")
    for folder in [malignant_folder, benign_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            patient_id = row["patient_id"]
            pathology = row["pathology"]

            if pathology.lower() == "malignant":
                destination_folder = os.path.join(malignant_folder, patient_id)
            elif pathology.lower() == "benign":
                destination_folder = os.path.join(benign_folder, patient_id)
            else:
                print(f"Unknown pathology: {pathology}")
                continue

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            for image_type in ["image_path", "cropped_path", "masked_path"]:
                image_path = row[image_type]
                try:
                    if "cropped" in image_type:
                        new_filename = "cropped_image"
                    elif "masked" in image_type:
                        new_filename = "masked_image"
                    else:
                        new_filename = "image"
                    shutil.move(image_path, os.path.join(destination_folder, new_filename))
                    print(f"Moved {new_filename} to {destination_folder}")
                except Exception as e:
                    print(f"Error moving {image_path}: {e}")

csv_file_path = "data_result.csv"
root_folder = r"D:\Project\dataset_processing\test"
move_files(csv_file_path, root_folder)
