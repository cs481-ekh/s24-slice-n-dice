from ipywidgets import AppLayout, Button, VBox, Layout, HBox, Output, RadioButtons
import matplotlib.pyplot as plt

# Define selected_option as a global variable with a default value
selected_option = 'Static Image'

def display_cube(cube):
    global selected_option 
    
    with large_box:  # Capture output within large_box
        # Clear previous content
        large_box.clear_output(wait=True)
        
        if selected_option == 'Static Image':
            display_static_image(cube)
        elif selected_option == 'Option 2':
            display_option_2(cube)
        elif selected_option == 'Option 3':
            display_option_3(cube)

        else:
            print("failing here")

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

def display_option_2(cube):
    # Function to display option 2
    pass

def display_option_3(cube):
    # Function to display option 3
    pass

def handle_radio_button_change(change):
    global selected_option  # Declare selected_option as a global variable
    
    selected_option = change['new']
    display_cube(cube_data)
    
def display_app(large_box):
    # Define radio buttons
    options = ['Static Image', 'Option 2', 'Option 3']
    radio_buttons = RadioButtons(options=options, index=0)  # Setting index to 0 for default selection
    
    # Attach callback function to handle changes
    radio_buttons.observe(handle_radio_button_change, names='value')
    
    # Create a VBox for radio buttons
    radio_buttons_container = VBox([radio_buttons])
    
    # Create HBox for large box and radio buttons container
    boxes_hbox = HBox([large_box, radio_buttons_container])
    
    # Define other buttons
    slim_bar = Button(description="Slim Bar", 
                      layout=Layout(width="50%", height="20px"))
    
    # Create AppLayout
    app_layout = AppLayout(header=None,
                           left_sidebar=None,
                           center=VBox([boxes_hbox]),  # Remove output widget from center
                           right_sidebar=None,
                           footer=slim_bar,
                           pane_heights=['20px', 1, '20px'])
    
    # Display the layout
    display(app_layout)

# Create a large_box
large_box = Output(layout=Layout(width="70%", height="300px"))

# Call display_app to display the app layout
display_app(large_box)