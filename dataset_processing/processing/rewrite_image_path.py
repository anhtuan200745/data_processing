import os
import csv
import pydicom
import shutil

csv_path = "mass_case_description_test_set_mini.csv"


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

    return None


def check_masked_image(file_path):
    masked = False
    file_data = pydicom.dcmread(file_path)

    pixel_data = file_data.pixel_array

    max_pixel_value = pixel_data.max()
    min_pixel_value = pixel_data.min()

    if max_pixel_value == 255 and min_pixel_value == 0:
        masked = True
        return masked
    else:
        return masked


def move_and_rename_image(image_path, folder_path):
    patient_id = extract_patient_id(image_path)
    pathology = find_pathology(patient_id, csv_path)

    if "test" in image_path.lower():
        subfolder = "test"
    elif "training" in image_path.lower():
        subfolder = "training"
    else:
        subfolder = ""

    subfolder_path = os.path.join(folder_path, subfolder)
    pathology_path = os.path.join(subfolder_path, pathology)
    if not os.path.exists(pathology_path):
        os.makedirs(pathology_path)

    if "_1" in image_path:
        if check_masked_image(image_path):
            image_name_base = patient_id + "_masked_image"
        else:
            image_name_base = patient_id + "_cropped_image"
    else:
        image_name_base = patient_id + "_image"

    existing_files = [file for file in os.listdir(pathology_path) if image_name_base in file]

    count = len(existing_files)

    if count > 0:
        image_name = f"{image_name_base}_{count + 1}{os.path.splitext(image_path)[1]}"
    else:
        image_name = f"{image_name_base}{os.path.splitext(image_path)[1]}"
    new_image_path = os.path.join(pathology_path, image_name)

    shutil.move(image_path, new_image_path)

    print(f"Image moved and renamed to {new_image_path}")


def rewrite(root_folder):
    if not os.path.exists(root_folder):
        print("Root folder not found.")
        return
    moved_file = 0
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.dcm'):
                file_path = os.path.join(root, file)
                move_and_rename_image(file_path, "D:\\Project\\dataset_processing\\BreastCancer")
                moved_file += moved_file
    return moved_file


def main():
    root_folder = "D:/Project/dataset_processing/CBIS-DDSM"
    print(rewrite(root_folder))


if __name__ == "__main__":
    main()
