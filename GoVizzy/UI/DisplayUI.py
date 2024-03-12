from widgets import slice_x_slider, slice_y_slider, slice_z_slider
import ipywidgets as widgets
from ipywidgets import Dropdown, VBox, HBox, Output, ColorPicker, AppLayout, Layout, Label, Button
import ipyvolume as ipv
import matplotlib.pyplot as plt
import GoVizzy.plotting

# Define globals
selected_option = 'Volumetric'
options = ['Static Image', 'Grid Points', 'Volumetric']
dropdown = Dropdown(options=options, value=options[2], description='Options:')
large_box = Output(layout=Layout(width="75%", height="100px"))
additional_box = Output(layout=Layout(width="200px", height="300px"))
slice_picker = Output(layout=Layout(width="200px", height="100px", border='1px solid black'))
slice_picker_descr = widgets.Label(value="Slice Picker", layout=Layout(margin='5px 0 0 5px'))
exit_button = widgets.Button(description='[X]', button_style='danger')
exit_button.layout.margin = '0 0 0 auto'  # Add margin to the left to push it to the right


newCube_button = Button(description='New Cube Button', layout=Layout(width="200px", height="100px", border='1px solid black'))
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

        image_path = './gv.png'  
        image_data = plt.imread(image_path)
        plt.figure()
        plt.imshow(image_data)
        plt.axis('off')  
        plt.show()
     

def show_ui():
    
    large_box.layout.visibility = 'visible'
    additional_box.layout.visibility = 'visible'
    dropdown.layout.visibility = 'visible'
    slice_picker.layout.visibility = 'visible'
    slice_picker_descr.layout.visibility = 'visible'
    newCube_button.layout.visibility = 'visible'

def display_cube(cube):
    
    with large_box:  # Capture output within large_box
        # Clear previous content
        large_box.clear_output()
        large_box.layout = Layout(width="85%", height="70%")

        
        if selected_option == 'Static Image':
            display_static_image(cube)
        elif selected_option == 'Grid Points':
            display_cell_data(cube)
        elif selected_option == 'Volumetric':
            display_ipyvolume_plot(cube)
        else:
            print("Invalid option selected")

def display_static_image(cube):
    # Extract the cube data
    data3D = cube.data3D

    # Create a meshgrid for plotting
    x, y, z = cube.grid[0], cube.grid[1], cube.grid[2]

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

def display_cell_data(cube):
    # Function to display cell data directly in the additional widget box
    with additional_box:
        additional_box.clear_output(wait=True)
        visualizer = GoVizzy.plotting.Visualizer(cube)
        visualizer.display_cell_data()

def display_ipyvolume_plot(cube):
    #data3D = cube.data3D
    #ipv.figure()
    #ipv.pylab.volshow(data3D)
    with large_box:
        #ipv.show()
        visualizer = GoVizzy.plotting.Visualizer(cube)
        visualizer.display_cell_slices()


def display_app(large_box, additional_box):
    # Attach the dropdown change handler
      
    # Create a VBox for dropdown
    dropdown_container = VBox([dropdown])
    # Combine the Output widgets with their descriptions
    slice_box = VBox([slice_picker_descr, slice_picker])
        
    # Attach callback function to button click event
    
    
    menu_options = VBox([dropdown, slice_box, additional_box, slice_x_slider, slice_y_slider, slice_z_slider, newCube_button], layout=Layout(flex='1'))
    display_box = HBox([large_box, menu_options])
    
    
    slim_box = HBox([ exit_button])
    slim_box.layout.width = '100%'
    slim_box.layout.height = '20px'
    
    slim_box.layout.justify_content = 'space-between'

    # Define other buttons
    #slim_bar = ColorPicker(concise=True, value='blue', description='Color', disabled=False, layout=Layout(width="50%", height="20px"))
    large_box = Output(layout=Layout(width="75%", height="500px"))
    # Create AppLayout
    app_layout = AppLayout(header=slim_box, left_sidebar=None, center=display_box,
                           footer=None, pane_heights=['20px', 1, '20px'])
    
    # Display the layout
    display(app_layout)

# Call the display_app function
display_app(large_box, additional_box)

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
    
    # Update the app layout
   

    dropdown.observe(handle_dropdown_change, names='value')
