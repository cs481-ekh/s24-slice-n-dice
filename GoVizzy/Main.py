import fileInput
import UI.DisplayUI
import ipywidgets as widgets
import os
import cube_viskit as cv
import matplotlib.pyplot as plt
from ipywidgets import AppLayout, Button, VBox, Layout, HBox, Output
from IPython.display import display

# Define a text input widget
file_input = widgets.Text(description='File Name:')

# Define a submit button widget
submit_button = widgets.Button(description='Submit')

# Define the app layout

large_box = Output(layout=Layout(width="70%", height="300px"))
# Function to handle submit button click
def submit_button_clicked(b):
    directory = "./"
    fileName = file_input.value.strip()
    if fileName.endswith('.cube'):
        source_path = fileInput.find_source_path(fileName, directory)
        if source_path:
            print(f"Source file found: {source_path}")
            unique_file_name = fileInput.generate_unique_filename(fileName, directory)
            destination_path = os.path.join(directory, unique_file_name)
            success = fileInput.copy_file(source_path, destination_path)
            if success:
                new_cube = cv.Cube()
                new_cube.load_cube(destination_path)
                UI.DisplayUI.display_cube(new_cube)
                UI.DisplayUI.display_app(large_box)  # Display the app layout
                file_input.layout.visibility = 'hidden'  # Hide the file input widget
                submit_button.layout.visibility = 'hidden'  # Hide the submit button widget
        else:
            print(f"Source file not found: {fileName}")
    else:
        print("Enter a valid .cube file name")

# Attach button click handler
submit_button.on_click(submit_button_clicked)

# Display the widgets
display(widgets.VBox([file_input, submit_button]))