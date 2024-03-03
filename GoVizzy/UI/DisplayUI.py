from ipywidgets import Dropdown, VBox, HBox, Output, ColorPicker, AppLayout, Layout
import ipyvolume as ipv
import matplotlib.pyplot as plt
import UI.plotting  # Import the necessary module containing display_cell_data

# Define selected_option as a global variable with a default value
selected_option = 'Static Image'

# Define dropdown options
options = ['Static Image', 'Grid Points', 'Volumetric']

# Create the dropdown menu
dropdown = Dropdown(options=options, value=options[0], description='Options:')

# Define large_box and additional_box
large_box = Output(layout=Layout(width="70%", height="500px"))
additional_box = Output(layout=Layout(width="30%", height="300px"))

def display_cube(cube):
    
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
        visualizer = UI.plotting.Visualizer(cube)
        visualizer.display_cell_data()

def display_ipyvolume_plot(cube):
    data3D = cube.data3D
    ipv.pylab.volshow(data3D, lighting=False, data_min=None, data_max=None, max_shape=256, tf=None, stereo=False, ambient_coefficient=0.5, diffuse_coefficient=0.8, specular_coefficient=0.5, specular_exponent=5, downscale=1, level=[0.1, 0.5, 0.9], opacity=[0.01, 0.05, 0.1], level_width=0.1, controls=True, max_opacity=0.2, memorder='C', extent=None, description=None)
    # Embed the plot in the large_box widget
    with large_box:
        ipv.show()

def handle_dropdown_change(change, cube):
    global selected_option
    selected_option = change.new
    
    # Clear the output
    with large_box:
        large_box.clear_output(wait=True)
    
    # Display the cube based on the selected option
    display_cube(cube)

def display_app(large_box, additional_box):
    # Attach the dropdown change handler
    dropdown.observe(handle_dropdown_change, names='value')
    
    # Create a VBox for dropdown
    dropdown_container = VBox([dropdown])
    
    # Create VBox for additional box and dropdown container
    vbox_dropdown_additional = VBox([dropdown, additional_box])
    
    # Create HBox for large box and VBox containing dropdown and additional box
    hbox_large_dropdown_additional = HBox([large_box, vbox_dropdown_additional])
    
    # Define other buttons
    slim_bar = ColorPicker(concise=True, value='blue', description='Color', disabled=False, layout=Layout(width="50%", height="20px"))
    
    # Create AppLayout
    app_layout = AppLayout(header=None, left_sidebar=None, center=hbox_large_dropdown_additional,
                           footer=slim_bar, pane_heights=['20px', 1, '20px'])
    
    # Display the layout
    display(app_layout)

# Call the display_app function
display_app(large_box, additional_box)