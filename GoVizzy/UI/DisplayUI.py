import ipywidgets as widgets
from ipywidgets import Dropdown, VBox, HBox, Output, ColorPicker, AppLayout, Layout, Label
import ipyvolume as ipv
import matplotlib.pyplot as plt
import GoVizzy.plotting  
from UI import windowManager

additional_box = Output(layout=Layout(width="200px", height="300px"))
def display_cube(cube):
    large_box = Output(layout=Layout(width="50%", height="50%"))
    with large_box:  # Capture output within large_box
        # Clear previous content
        large_box.clear_output(wait=True)
        
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
        visualizer.display_cell()


def display_app():
    # Attach the dropdown change handler
    app_layout = windowManager.LayoutManager(None,None,None,None)
    options = ['Static Image', 'Grid Points', 'Volumetric']
    dropdown = Dropdown(options=options, value=options[2], description='Options:')
    slice_picker = Output(layout=Layout(width="200px", height="100px", border='1px solid black'))
    slice_picker_descr = widgets.Label(value="Slice Picker", layout=Layout(margin='5px 0 0 5px'))
    newCube = Output(layout=Layout(width="200px", height="100px", border='1px solid black'))
    newCube_descr = widgets.Label(value="New Cube", layout=Layout(margin='5px 0 0 5px'))
    # Create a VBox for dropdown
    dropdown_container = VBox([dropdown])
    # Combine the Output widgets with their descriptions
    slice_box = VBox([slice_picker_descr, slice_picker])
    newCube_box = VBox([newCube_descr, newCube])
    center_widget = Output(layout=Layout(width="75%", height="500px"))
    menu_options = VBox([dropdown, slice_box, additional_box, newCube_box])
    #display_box = HBox([large_box, menu_options])
    
    

    # Define other buttons
    slim_bar = ColorPicker(concise=True, value='blue', description='Color', disabled=False, layout=Layout(width="50%", height="20px"))
    
    # Create AppLayout
    app_layout.update_layout(None, center_widget, menu_options, slim_bar)
    
    # Display the layout
    display(app_layout.initial_layout)

# Call the display_app function
#display_app(large_box, additional_box)


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
