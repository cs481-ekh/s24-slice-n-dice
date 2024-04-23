"""
This module provides functionality to display output widgets for GoVizzy.
"""

import ipywidgets as widgets
from ipywidgets import Dropdown, VBox, HBox, Output, ColorPicker, AppLayout, Layout, Label, Button, Checkbox, link, Accordion
import ipyvolume as ipv
import matplotlib.pyplot as plt
from gv_ui import plotting, meshes, gvWidgets
from gv_ui.gvWidgets import mesh_visibility_toggle, atom_color_picker, atom_scale_slider, bond_visibility_toggle, bond_color_picker, bond_scale_slider
from IPython.display import display

# Define globals
selected_option ='Slice Options'
options = ['Slice Options', 'Mesh Options'] 
dropdown = Dropdown(options=options, value=options[0], layout=Layout(margin='5px 0 0 5px'));
large_box = Output(layout=Layout(width="70%", height="100%"))
selected_view_options = Output(layout=Layout(width="auto", height="300px"))
slice_picker = Output(layout=Layout(flex= '1',border='1px solid black'))
slice_picker_descr = widgets.Label(value="Slice Picker", layout=Layout(margin='5px 0 0 5px'))
exit_button = widgets.Button(description='[X]', button_style='danger',border='1px solid black')
exit_button.layout.margin = '0 0 0 auto'  # Add margin to the left to push it to the right
in_app_exit = widgets.Button(description='[X]', button_style='danger',border='1px solid black')

newCube_button = Button(description='New Cube', layout=Layout(flex= '1',  border='1px solid black'))
save_button = Button(description='Save', layout=Layout(flex= '1',  border='1px solid black'))

# atom mesh globals
atom_meshes = []

# visualizer global
visualizer = None

def show_menu():
    """
    Displays logo and hides the app output.
    """

    exit_button.layout.visibility = 'visible'
    selected_view_options.layout.visibility = 'hidden'
    dropdown.layout.visibility = 'hidden'
    slice_picker.layout.visibility = 'hidden'
    slice_picker_descr.layout.visibility = 'hidden'
    newCube_button.layout.visibility = 'hidden'
    with large_box:
        # Clear previous content
        large_box.clear_output(wait=True)
        large_box.layout = Layout(width="100%", height="85%", justify_content="center", margin="0 0 5% 40%")

        image_path = './gv_ui/gv.png'  
        image_data = plt.imread(image_path)
        plt.figure()
        plt.imshow(image_data)
        plt.axis('off')  
        plt.show()
   # display_app()

def show_ui():
    """
    Sets the visibility of the GoVizzy output widgets to visible.
    """

    large_box.layout.visibility = 'visible'
    selected_view_options.layout.visibility = 'visible'
    dropdown.layout.visibility = 'visible'
    slice_picker.layout.visibility = 'visible'
    slice_picker_descr.layout.visibility = 'visible'
    newCube_button.layout.visibility = 'visible'

def display_cube(cube):
    """
    Displays the cube plot based on the value of the dropdown.
    """

    global atom_meshes, visualizer
    visualizer = plotting.Visualizer(cube)
    with large_box:  # Capture output within large_box
        # Clear previous content
        large_box.clear_output()
        large_box.layout = Layout(width="75%", height="100%")
        
        # Slice View
        if selected_option == 'Slice Options':
            visualizer.display_cell_slices()
            
        # Mesh View
        elif selected_option == 'Mesh Options':
            visualizer.display_cell()
            atom_meshes = meshes.plot_atoms(cube)
            meshes.plot_bonds(cube)

        # Additional View   
        elif selected_option == 'Color Options':
            visualizer.display_cell()
            
        else:
            print("Invalid option selected")
        


def display_app():
    """
    Displays the ipvolume.Figure and sets the sidebar options.
    """

    # Containers for right menu 
    global atom_meshes, visualizer
    top_container = HBox([dropdown, in_app_exit])
    bottom_container = HBox([newCube_button])
    bottom_container_vbox= VBox([bottom_container], layout=Layout(align_self='flex-end'))
   
    with selected_view_options:
        selected_view_options.clear_output()
        figure_controls = visualizer.figure.volumes[0].tf.control()
        # Combine the Output widgets with their descriptions
        if selected_option == 'Slice Options':
            #display slidersss TO DO 
            slice_box = VBox([slice_picker_descr,
                              gvWidgets.slice_x_slider,
                              gvWidgets.slice_x_check,
                              gvWidgets.slice_y_slider,
                              gvWidgets.slice_y_check,
                              gvWidgets.slice_z_slider,
                              gvWidgets.slice_z_check,
                              gvWidgets.slice_color,
                              figure_controls,])
            display(slice_box)
            
            
        
        
        elif selected_option == 'Mesh Options':
            #display Mesh TO DO
            atom_controls = []
            for mesh in atom_meshes:
                controls = [mesh_visibility_toggle(mesh, 'Visible'),
                        atom_color_picker(mesh, 'Color'),
                        atom_scale_slider(mesh, 'Scale')]
                atom_controls.append(VBox(children=controls))
            titles = tuple(f'Atom {idx}' for idx in range(len(atom_controls)))
            
            accordion = Accordion(children=atom_controls, titles=titles)
            mesh_box = VBox([accordion,
                             gvWidgets.bond_visibility_toggle,
                             gvWidgets.bond_color_picker,
                             gvWidgets.bond_scale_slider,
                             figure_controls])
            display(mesh_box)
                
        
        
        else:
            print("Invalid option selected")

    # Display the layout
    view_bar = VBox([top_container, selected_view_options, bottom_container_vbox], 
                layout=Layout(flex='1', height='500px'))
       
    display_box = HBox([large_box, view_bar])
    app_layout = AppLayout(header=None, left_sidebar=None, center=display_box,
                           footer=None, pane_heights=['20px', 1, '20px'])
    
    display(app_layout)

# Call the display_app function

display_app()


def clear_all_outputs():
    """
    Clears the output of the GoVizzy widgets and sets their visibilities to 
    hidden.
    """
    large_box.clear_output()
    selected_view_options.clear_output()
    slice_picker.clear_output()
    newCube_button.layout.visibility = 'hidden'
    exit_button.layout.visibility = 'hidden'
    slice_picker.layout.visibility = 'hidden'
    slice_picker_descr.layout.visibility = 'hidden'
    dropdown.layout.visibility = 'hidden'
    in_app_exit.layout.visibility = 'hidden'
    save_button.layout.visibility= 'hidden'
    
    with large_box:
        exit_message = widgets.Textarea(value='Please restart the terminal and "%run Main.py" to continue use', disabled=True)
   
        display(exit_message)
    
def handle_dropdown_change(change, cube):
    """
    Sets the selected option to the value of the dropdown.
    """

    global selected_option
    selected_option = change.new
    
    # Clear the output
    with large_box:
        large_box.clear_output(wait=True)
    
    # Display the cube based on the selected option
    
    display_cube(cube)
    display_app() 
    
  
