import os
import shutil
import cube_viskit as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


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

# Function to display cube
def display_cube(cube):
        # Extract the cube data
        data3D = new_cube.data3D
        
        # Create a meshgrid for plotting
        x, y, z = new_cube.grid[0], new_cube.grid[1], new_cube.grid[2]
        
        # Create a figure and 3D axes
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot cube data
        ax.scatter(x, y, z, c=data3D.flatten(), cmap='viridis')
        
        # Set axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Show plot
        plt.show()


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
        # Copy the file
        if copy_file(source_path, destination_path):
            # Load the cube data
            new_cube = cv.Cube()
            new_cube.load_cube(destination_path)
            
            # Visualize cube data
            display_cube(new_cube)
     
    else:
        print(f"Source file not found: {fileName}")


