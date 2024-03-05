import os
import shutil
import cube_viskit as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to find the source file path based on the file name
def find_source_path(fileName, directory):
   
    for root, dirs, files in os.walk(directory):
        if fileName in files:
            # Return the full path of the file
            return os.path.join(root, fileName)
    
    # If the file is not found
    return None

# Function to generate a unique file name with an ascending number
def generate_unique_filename(fileName, directory):
    # If the file already exists in the destination directory, append an ascending number
    counter = 1
    while True:
        # Generate the new file name with the counter appended
        new_file_name = f"{os.path.splitext(fileName)[0]}_{counter}.cube"
        destination_path = os.path.join(directory, new_file_name)
        
        # If the file does not exist, return the new file name
        if not os.path.exists(destination_path):
            return new_file_name
        
        # Increment the counter
        counter += 1

# Function to copy a file from source to destination
def copy_file(source_path, destination_path):
    try:
        # Copy the file from source to destination
        shutil.copyfile(source_path, destination_path)
        print(f"File copied: {destination_path}")
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

