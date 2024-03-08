import ipywidgets as widgets
import fileInput
import ipywidgets as widgets
import os
import cube_viskit as cv
import matplotlib.pyplot as plt
from ipywidgets import AppLayout, Button, HBox, Layout, HBox, Output, Dropdown, VBox
from IPython.display import display

class LayoutManager:
    def __init__(self, left_widget, center_widget, right_widget, footer):
        self.left_widget = left_widget
        self.center_widget = center_widget
        self.right_widget = right_widget
        
        exit_button = widgets.Button(description='[X]', button_style='danger')
        exit_button.layout.margin = '0 0 0 auto'  
        
        self.header = VBox([exit_button])
        self.footer = footer
        self.initial_layout = self._create_initial_layout()
   
    def _create_initial_layout(self):
        """
        Create the initial AppLayout with specified widgets.

        Returns:
            AppLayout: The initialized AppLayout.
        """
        # Create the initial AppLayout
        initial_layout = widgets.AppLayout(
            left_sidebar = self.left_widget,
            center = self.center_widget,
            right_sidebar = self.right_widget,
            header = self.header, 
            footer = None,
            height = "100%", 
            width = "100%",
            layout = Layout(flex='1')
        ) 
        
        return initial_layout


    def update_layout(self, new_left, new_center, new_right, new_foot):
        if new_left is not None:
            self.left_widget = new_left
        if new_center is not None:
            self.center_widget = new_center
        if new_right is not None:
            self.right_widget = new_right
        if new_foot is not None:
            self.footer = new_right
        
        self.initial_layout = self._create_initial_layout()

def displayMenu():
    # Create menu layout
    center_widget = Output(layout=Layout(width="50%", height="50%",justify_content = "center", margin="0 0 5% 40%"))
    with center_widget:
    # Clear previous content
        center_widget.clear_output(wait=True)
        image_path = './gv.png'  
        image_data = plt.imread(image_path)
        plt.figure()
        plt.imshow(image_data)
        plt.axis('off')  
        plt.show()

  
    menu = LayoutManager(None, center_widget, None, None)
    display(menu.initial_layout)
   
    



