import os
import shutil

# Function to check if file is '.cube'
def validate_name(fileName):
    while not fileName.endswith('.cube'):
        print("Enter a valid .cube file name: ")
        fileName = input()
    return fileName
        
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
# CHANGE THIS TO SEND TO PARSER?
# Function to copy a file from source to destination
def copy_file(source_path, destination_path):
    try:
        # Copy the file from source to destination
        shutil.copyfile(source_path, destination_path)
        print(f"File copied: {destination_path}")
    except Exception as e:
        print(f"Error copying file: {e}")

# TODO: add to GoVizzy.pynb instead? using this to run 
if __name__ == "__main__":
    directory = "./"
    
    # Prompt the user for a valid file name
    fileName = input("Enter a valid .cube file name: ")
    fileName = validate_name(fileName)
    
    # Find the source file path
    source_path = find_source_path(fileName, directory)
    if source_path:
        print(f"Source file found: {source_path}")
        
        # Generate a unique file name if needed 
        unique_file_name = generate_unique_filename(fileName, directory)
        destination_path = os.path.join(directory, unique_file_name)
        
        # Copy the file
        copy_file(source_path, destination_path)
    else:
        print(f"Source file not found: {fileName}")


