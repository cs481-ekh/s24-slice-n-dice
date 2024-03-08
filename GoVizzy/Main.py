import fileInput
import ipywidgets as widgets
import os
import cube_viskit as cv
import matplotlib.pyplot as plt
from ipywidgets import AppLayout, Button, HBox, Layout, HBox, Output, Dropdown
from IPython.display import display
from UI import windowManager, DisplayUI




# Define a text input widget
file_input = widgets.Text(description='File Name:')

# Define a submit button widget
submit_button = widgets.Button(description='Submit')

# Define the app layout
options = ['Static Image', 'Grid Points', 'Volumetric']


def handle_submit_button_clicked(b):
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
                
                DisplayUI.display_cube(new_cube)
                DisplayUI.display_app() 
                #DisplayUI.display_cell_data(new_cube)
                file_input.layout.visibility = 'hidden'  # Hide the file input widget
                submit_button.layout.visibility = 'hidden'  # Hide the submit button widget

         #   DisplayUI.dropdown.observe(
          #          lambda change: DisplayUI.handle_dropdown_change(change, new_cube),
           #         names='value'
            #    )
                
        else:
            print(f"Source file not found: {fileName}")
    else:
        print("Enter a valid .cube file name")

def main():
    global file_input, submit_button
    #windowManager.displayMenu()
    # Define a text input widget
    file_input = widgets.Text(description='File Name:')

    # Define a submit button widget
    submit_button = widgets.Button(description='Submit')

    # Attach button click handler
    submit_button.on_click(handle_submit_button_clicked)

    # Display the widgets
    file_input_button = HBox((file_input, submit_button), layout=Layout(justify_content='center'))


    
    display(file_input_button)

# Call the main function
if __name__ == "__main__":
    main()

