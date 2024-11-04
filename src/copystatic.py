import os
import shutil

def copy_over_directory(source, destination):
    # delete all destination directory contents
    # copy all files and subdirectories from the source directory to the destination directory
    if not os.path.exists(destination):
        os.mkdir(destination)

    s_contents = os.listdir(source)

    for item in s_contents:
        from_path = f"{source}/{item}"
        if os.path.isfile(from_path):
            shutil.copy(from_path, destination)
            print(f"{item} copied to {destination}")
        elif os.path.isdir(from_path):
            copy_over_directory(from_path, f"{destination}/{item}")