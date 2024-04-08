import ipywidgets as widgets
from ipywidgets import Dropdown, VBox, HBox, Output, ColorPicker, AppLayout, Layout, Label, Button, Checkbox, link, Accordion
import ipyvolume as ipv
import matplotlib.pyplot as plt
from gv_ui import plotting, meshes, gvWidgets
from gv_ui.gvWidgets import mesh_visibility_toggle, atom_color_picker
from IPython.display import display

# Define globals
selected_option ='Slice Options'
options = ['Slice Options', 'Mesh Options'] #, 'Color Options']
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

# Displays logo and hides the app output
def show_menu():
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
    
    large_box.layout.visibility = 'visible'
    selected_view_options.layout.visibility = 'visible'
    dropdown.layout.visibility = 'visible'
    slice_picker.layout.visibility = 'visible'
    slice_picker_descr.layout.visibility = 'visible'
    newCube_button.layout.visibility = 'visible'

def display_cube(cube):
    global atom_meshes
    visualizer = plotting.Visualizer(cube)
    global atom_meshes
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

        # Additional View   
        elif selected_option == 'Color Options':
            visualizer.display_cell()
            
        else:
            print("Invalid option selected")
        


def display_app():
    
    # Containers for right menu 
    global atom_meshes
   
    top_container = HBox([dropdown, in_app_exit])
    
    bottom_container = HBox([newCube_button, save_button])
   
    # Combine the Output widgets with their descriptions
    if selected_option == 'Slice Options':
        #display slidersss TO DO 
        with selected_view_options:
            selected_view_options.clear_output()
            slice_box = VBox([slice_picker_descr, gvWidgets.slice_x_slider, gvWidgets.slice_x_check, gvWidgets.slice_y_slider, gvWidgets.slice_y_check, gvWidgets.slice_z_slider, gvWidgets.slice_z_check])
            display(slice_box)
        
        
    
    
    elif selected_option == 'Mesh Options':
        #display Mesh TO DO
        atom_controls = []
        for mesh in atom_meshes:
            controls = [mesh_visibility_toggle(mesh, 'Visible'),
                    atom_color_picker(mesh, 'Color')]
            atom_controls.append(VBox(children=controls))
        titles = tuple(f'Atom {idx}' for idx in range(len(atom_controls)))
        with selected_view_options:
            selected_view_options.clear_output()
            accordion = Accordion(children=atom_controls, titles=titles)
            mesh_box = VBox([accordion])
            display(mesh_box)
        
    
    
    elif selected_option == 'Color Options':
        #ADD color controls here 
        with selected_view_options:
            selected_view_options.clear_output()
        
        
    
    
    
    else:
            print("Invalid option selected")
    
    # Display the layout
    view_bar = VBox([top_container, selected_view_options, bottom_container], layout=Layout(flex='1'))
       
    display_box = HBox([large_box, view_bar])
    app_layout = AppLayout(header=None, left_sidebar=None, center=display_box,
                           footer=None, pane_heights=['20px', 1, '20px'])
    
    display(app_layout)

# Call the display_app function

display_app()


def clear_all_outputs():
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
    global selected_option
    selected_option = change.new
    
    # Clear the output
    with large_box:
        large_box.clear_output(wait=True)
    
    # Display the cube based on the selected option
    
    display_cube(cube)
    display_app() 
    
  
