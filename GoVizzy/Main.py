import fileInput
import ipywidgets as widgets
import os
import cube_viskit as cv
import matplotlib.pyplot as plt
from ipywidgets import AppLayout, Button, HBox, Layout, HBox, Output, Dropdown
from IPython.display import display, clear_output
from UI import DisplayUI
import signal
import sys



# Define a text input widget
file_input = widgets.Text(description='File Name:')

# Define a submit button widget
submit_button = widgets.Button(description='Submit')

# Define the app layout
options = ['Static Image', 'Grid Points', 'Volumetric']

display_box = Output(layout=Layout(width="70%", height="100px"))
additional_box = Output(layout=Layout(width="30%", height="300px"))

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
                DisplayUI.show_ui()
                DisplayUI.display_cube(new_cube)
                DisplayUI.display_app(display_box, additional_box) 
                DisplayUI.display_cell_data(new_cube)
                file_input.layout.visibility = 'hidden'  # Hide the file input widget
                submit_button.layout.visibility = 'hidden'  # Hide the submit button widget


            # Handlers for dropdown change and button clicks
            DisplayUI.dropdown.observe(
                    lambda change: DisplayUI.handle_dropdown_change(change, new_cube),
                    names='value'
                )
            DisplayUI.newCube_button.on_click(handle_newCube_click)
            
                
        else:
            print(f"Source file not found: {fileName}")
    else:
        print("Enter a valid .cube file name")



def handle_exit_click(b):
    file_input.layout.visibility = 'hidden'  # Hide the file input widget
    submit_button.layout.visibility = 'hidden'  # Hide the submit button widget
    DisplayUI.clear_all_outputs()

    exit_message = widgets.Textarea(value='Please restart the terminal.', disabled=True,
                              layout=Layout(width="50%", height="100px"))
    display(exit_message)

def handle_newCube_click(b):
    DisplayUI.show_menu()
    file_input.layout.visibility = 'visible'
    submit_button.layout.visibility = 'visible'
    
def main():
    global file_input, submit_button
    
    DisplayUI.show_menu()
    # Define a text input widget
    file_input = widgets.Text(description='File Name:')

    # Define a submit button widget
    submit_button = widgets.Button(description='Submit')

    # Attach button click handler
    submit_button.on_click(handle_submit_button_clicked)

    # Display the widgets
    file_input_button = HBox((file_input, submit_button), layout=Layout(justify_content='center'))

    DisplayUI.exit_button.on_click(handle_exit_click)
    
    display(file_input_button)

# Call the main function
if __name__ == "__main__":
    main()

