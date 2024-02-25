import os
from cube_viskit import Cube
import ipywidgets as widgets
from IPython.display import display

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
        row = "<tr>"
        row = "<th>"+key+"</th>"
        for entry in data:
            row += "<td>"+entry+"</td>"
        row += "</tr>"
        return row

    @staticmethod
    def __horizontal_row(key: str, data: list[str]):
        row = "<tr>"
        for entry in data:
            row += "<td>"+entry+"</td>"
        row += "</tr>"
        return row

    @staticmethod
    def __create_table_html(table_data: dict[str, list[str]], vertical: bool=False):
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
        titles = ['Data', 'Cell']
        data = {
            "File Name": [os.path.basename(self.cube.fname)],
            "Prefix": [self.cube.prefix],
            "Scaling Factor": [str(self.cube.scaling_factor)],
            "Units": [self.cube.units],
        }
        data_table = widgets.HTML(
            value=Visualizer.__create_table_html(data, vertical=True))
        cell = {
            "Symbols": [str(self.cube.atoms.symbols)],
            "Periodic Boundary Conditions": [str(self.cube.atoms.pbc)],
            "Cell Vectors": [str(self.cube.cell)],
            "Origin": [str(self.cube.origin)],
        }
        cell_table = widgets.HTML(
            value=Visualizer.__create_table_html(cell, vertical=True)
        )
        children = [data_table, cell_table]
        tab = widgets.Tab(children=children, titles=titles)
        display(tab)