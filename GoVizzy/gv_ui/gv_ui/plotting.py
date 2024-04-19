import os
from cube_viskit import Cube
import ipywidgets as widgets
import ipyvolume as ipv
from IPython.display import display
from gv_ui import gvWidgets
import matplotlib.pyplot as plt

class Visualizer:
    """
    A visualization class to create and display widgets from a provided Cube object.

    cube: cube_viskit.Cube
        Cube object created from the parsing of a .cube file.
    """

    cube: Cube

    def __init__(self, cube: Cube):
        self.cube = cube

    @staticmethod
    def __vertical_row(key: str, data: list[str]):
        """
        Creates a string in the format <tr><th>{key}</th><td>{data[i]}</td></tr>
        for all entries in the list data.
        """
        row = "<tr>"
        row = "<th>"+key+"</th>"
        for entry in data:
            row += "<td>"+entry+"</td>"
        row += "</tr>"
        return row

    @staticmethod
    def __horizontal_row(key: str, data: list[str]):
        """
        Creates a string in the format <tr><td>{data[i]}</td></tr> for all
        entries in the list data. The key is unused.
        """
        row = "<tr>"
        for entry in data:
            row += "<td>"+entry+"</td>"
        row += "</tr>"
        return row

    @staticmethod
    def __create_table_html(table_data: dict[str, list[str]], vertical: bool=False):
        """
        Creates an HTML <table></table> for all the keys in the table_data dict.
        Creates the rows based on if the vertical bool is true or false using
        the self.__horizontal_row() method if false otherwise
        self.__vertical_row().
        """
        create_row = Visualizer.__vertical_row if vertical else Visualizer.__horizontal_row
        table = "<table>"
        if not vertical:
            for key in table_data:
                table += "<th>" + key + "</th>"
        for key in table_data:
            table += create_row(key, table_data[key])
        table += "</table>"
        return table

    def display_cell_data(self):
        """
        Creates a tab widget returning the file name, prefix, scaling factor,
        units, symbols, periodic boundary conditions, cell vectors, and origin
        of the provided cell object.
        """
        cube = self.cube
        titles = ['Data', 'Cell']
        data = {
            "File Name": [os.path.basename(cube.fname)],
            "Prefix": [cube.prefix],
            "Scaling Factor": [str(cube.scaling_factor)],
            "Units": [cube.units],
        }
        data_table = widgets.HTML(
            value=Visualizer.__create_table_html(data, vertical=True))
        cell = {
            "Symbols": [str(cube.atoms.symbols)],
            "Periodic Boundary Conditions": [str(cube.atoms.pbc)],
            "Cell Vectors": [str(cube.cell)],
            "Origin": [str(cube.origin)],
        }
        cell_table = widgets.HTML(
            value=Visualizer.__create_table_html(cell, vertical=True)
        )
        children = [data_table, cell_table]
        tab = widgets.Tab(children=children, titles=titles)
        display(tab)

    def display_cell(self):
        """
        Displays the cube's data3D with the volshow() method.
        """
        cube = self.cube
        ipv.figure()
        transfer = ipv.pylab.transfer_function(level=[0.03, 0.5, 0.47], opacity=[0.05, 0.09, 0.1], level_width=0.1, controls=False)
        ipv.style.background_color(gvWidgets.color.value)
        ipv.pylab.volshow(cube.data3D, ambient_coefficient=0.8, lighting=True, tf=transfer, controls=False)
        ipv.show()
        
    def display_cell_slices(self):
        """
        Displays the cube's data3D with the volshow() method,
        and attach slices with textures set to the volume data. 
        """
        cube = self.cube
        fig = ipv.figure()
        transfer = ipv.pylab.transfer_function(level=[0.03, 0.5, 0.47], opacity=[0.05, 0.09, 0.1], level_width=0.1, controls=False)
        ipv.style.background_color(gvWidgets.color.value)
        volume = ipv.pylab.volshow(cube.data3D, ambient_coefficient=0.8, lighting=True, tf=transfer, controls=False)
        
        # Create planes, with textures set to the volume info        
        slice_x = ipv.plot_plane('x', volume=volume, description="Slice X", description_color="black", icon="mdi-knife", x_offset=70)
        slice_y = ipv.plot_plane('y', volume=volume, description="Slice Y", description_color="black", icon="mdi-knife", y_offset=70)
        slice_z = ipv.plot_plane('z', volume=volume, description="Slice Z", description_color="black", icon="mdi-knife", z_offset=70)
        
        widgets.jslink((gvWidgets.slice_x_slider, 'value'), (slice_x, 'x_offset'))
        widgets.jslink((gvWidgets.slice_y_slider, 'value'), (slice_y, 'y_offset'))
        widgets.jslink((gvWidgets.slice_z_slider, 'value'), (slice_z, 'z_offset'))
        
        widgets.jslink((gvWidgets.slice_x_check, 'value'), (slice_x, 'visible'))
        widgets.jslink((gvWidgets.slice_y_check, 'value'), (slice_y, 'visible'))
        widgets.jslink((gvWidgets.slice_z_check, 'value'), (slice_z, 'visible'))
        
        ipv.show()
        
        plt.style.use('_mpl-gallery-nogrid')

        fig, ax = plt.subplots()

        def update(w = 70):
            ax.imshow(cube.data3D[w])
            plt.show()

        widgets.interact(update, w=widgets.IntSlider(min=0, max=119, step=1, value=70))
