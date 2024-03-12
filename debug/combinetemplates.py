import os
import shutil

# Paths to your folders
folder1 = 'templates/extracted_cards/smalllog_rg'
folder2 = 'templates/extracted_cards/rand_loon'
folder3 = 'templates/extracted_cards/rand_egolem'
folder4 = 'templates/extracted_cards/combined'

# Create folder3 if it doesn't exist
os.makedirs(folder4, exist_ok=True)

# Function to copy files from source to destination folder
def copy_files(source, destination):
    for filename in os.listdir(source):
        source_file = os.path.join(source, filename)
        destination_file = os.path.join(destination, filename)

        # Check if the file doesn't already exist in the destination to avoid duplicates
        if not os.path.exists(destination_file):
            shutil.copy(source_file, destination_file)

# Copy files from folder1 and folder2 to folder3
copy_files(folder1, folder4)
copy_files(folder2, folder4)
copy_files(folder3, folder4)

print(f"Contents of {folder1} and {folder2} and {folder3} have been combined in {folder3}.")
