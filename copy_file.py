import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

def copy_file(file_path, target_directory):
    try:
        base_name, ext = os.path.splitext(file_path)
        ext = ext[1:] if ext else 'no_extension'
        ext_directory = os.path.join(target_directory, ext)

        if not os.path.exists(ext_directory):
            os.makedirs(ext_directory)

        shutil.copy(file_path, ext_directory)
    except Exception as exception:
        print(f"Error copying file {exception}")

def process_directory(source_directory, target_directory):
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(copy_file, file_path, target_directory)

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":

    source_directory = sys.argv[1]
    target_directory = sys.argv[2]

    if not os.path.exists(source_directory):
        print(f"{source_directory} does not exist.")
        sys.exit(1)

    create_directory_if_not_exists(target_directory)

    process_directory(source_directory, target_directory)