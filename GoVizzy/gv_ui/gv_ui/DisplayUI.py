import ipywidgets as widgets
from ipywidgets import Dropdown, VBox, HBox, Output, ColorPicker, AppLayout, Layout, Label, Button
import ipyvolume as ipv
import matplotlib.pyplot as plt
from gv_ui import plotting, meshes, gvWidgets

# Define globals
selected_option ='Slice Options'
options = ['Slice Options', 'Mesh Options', 'Color Options']
dropdown = Dropdown(options=options, value=options[0], layout=Layout(margin='5px 0 0 5px'));
large_box = Output(layout=Layout(width="70%", height="100%"))
additional_box = Output(layout=Layout(width="200px", height="300px"))
slice_picker = Output(layout=Layout(width="200px", height="100px", border='1px solid black'))
slice_picker_descr = widgets.Label(value="Slice Picker", layout=Layout(margin='5px 0 0 5px'))
exit_button = widgets.Button(description='[X]', button_style='danger')
exit_button.layout.margin = '0 0 0 auto'  # Add margin to the left to push it to the right

newCube_button = Button(description='New Cube', layout=Layout(width="200px", height="100px", border='1px solid black'))
# Displays logo and hides the app output
def show_menu():
  
    additional_box.layout.visibility = 'hidden'
    dropdown.layout.visibility = 'hidden'
    slice_picker.layout.visibility = 'hidden'
    slice_picker_descr.layout.visibility = 'hidden'
    newCube_button.layout.visibility = 'hidden'
    with large_box:
        # Clear previous content
        large_box.clear_output(wait=True)
        large_box.layout = Layout(width="100%", height="70%", justify_content="center", margin="0 0 5% 40%")

        image_path = './gv_ui/gv.png'  
        image_data = plt.imread(image_path)
        plt.figure()
        plt.imshow(image_data)
        plt.axis('off')  
        plt.show()
   # display_app()

def show_ui():
    
    large_box.layout.visibility = 'visible'
    additional_box.layout.visibility = 'visible'
    dropdown.layout.visibility = 'visible'
    slice_picker.layout.visibility = 'visible'
    slice_picker_descr.layout.visibility = 'visible'
    newCube_button.layout.visibility = 'visible'

def display_cube(cube):
    visualizer = plotting.Visualizer(cube)
    with large_box:  # Capture output within large_box
        # Clear previous content
        large_box.clear_output()
        large_box.layout = Layout(width="85%", height="100%")
        
        
        if selected_option == 'Slice Options':
            visualizer.display_cell_slices()
            
    
        elif selected_option == 'Mesh Options':
            visualizer.display_cell()
            origin = (50, 50, 50)
            radius = 10
            meshes.plot_sphere_surface(origin, radius)
            
        elif selected_option == 'Color Options':
            visualizer.display_cell()
            
        else:
            print("Invalid option selected")
        


def display_app():
    
    # Attach the dropdown change handler
      
    # Create a VBox for dropdown
    dropdown_container = VBox([dropdown])
    # Combine the Output widgets with their descriptions
    if selected_option == 'Slice Options':
        #display slidersss TO DO 
        with additional_box:
            additional_box.clear_output()
            slice_box = VBox([slice_picker_descr, gvWidgets.slice_x_slider, gvWidgets.slice_x_check, gvWidgets.slice_y_slider, gvWidgets.slice_y_check, gvWidgets.slice_z_slider, gvWidgets.slice_z_check])
            display(slice_box)
        menu_options = VBox([dropdown, additional_box, newCube_button], layout=Layout(flex='1'))
        display_box = HBox([large_box, menu_options])
    
        slim_box = HBox([ exit_button])
        slim_box.layout.width = '100%'
        slim_box.layout.height = '20px'
    
        slim_box.layout.justify_content = 'space-between'

    
        app_layout = AppLayout(header=slim_box, left_sidebar=None, center=display_box,
                           footer=None, pane_heights=['20px', 1, '20px'])
    
    elif selected_option == 'Mesh Options':
        #display Mesh TO DO 
        with additional_box:
            additional_box.clear_output()
            
        
        menu_options = VBox([dropdown, additional_box, newCube_button], layout=Layout(flex='1'))
        display_box = HBox([large_box, menu_options])
    
        slim_box = HBox([ exit_button])
        slim_box.layout.width = '100%'
        slim_box.layout.height = '20px'
    
        slim_box.layout.justify_content = 'space-between'

    
        app_layout = AppLayout(header=slim_box, left_sidebar=None, center=display_box,
                           footer=None, pane_heights=['20px', 1, '20px'])
    
    elif selected_option == 'Color Options':
        #ADD color controls here 
        with additional_box:
            additional_box.clear_output()
        
        menu_options = VBox([dropdown, additional_box, newCube_button], layout=Layout(flex='1'))
        display_box = HBox([large_box, menu_options])
    
        slim_box = HBox([ exit_button])
        slim_box.layout.width = '100%'
        slim_box.layout.height = '20px'
    
        slim_box.layout.justify_content = 'space-between'

    
        app_layout = AppLayout(header=slim_box, left_sidebar=None, center=display_box,
                           footer=None, pane_heights=['20px', 1, '20px'])
    
    else:
            print("Invalid option selected")
    
    # Display the layout
    display(app_layout)

# Call the display_app function

display_app()


def clear_all_outputs():
    large_box.clear_output()
    additional_box.clear_output()
    slice_picker.clear_output()
    newCube_button.layout.visibility = 'hidden'
    exit_button.layout.visibility = 'hidden'
    slice_picker.layout.visibility = 'hidden'
    slice_picker_descr.layout.visibility = 'hidden'
    dropdown.layout.visibility = 'hidden'
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
    
  
