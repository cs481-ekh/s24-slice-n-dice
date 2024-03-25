from gv_ui import gvWidgets
from cube_viskit import Cube
import ipywidgets as widgets
import ipyvolume as ipv
import numpy as np
from ase.units import Bohr 
from IPython.display import display

# taken from https://github.com/sweaver2112/periodic-table-data/blob/main/pTable.js
vanderwaals = {
    1: 12.0,
    2: 14.0,
    3: 18.2,
    6: 17.0,
    7: 15.5,
    8: 15.2,
    9: 14.7,
    10: 15.4,
    11: 22.7,
    12: 17.3,
    14: 21.0,
    15: 18.0,
    16: 18.0,
    17: 17.5,
    18: 18.8,
    19: 27.5,
    28: 16.3,
    29: 14.0,
    30: 13.9,
    31: 18.7,
    33: 18.5,
    34: 19.0,
    35: 18.5,
    36: 20.2,
    46: 16.3,
    47: 17.2,
    48: 15.8,
    49: 19.3,
    50: 21.7,
    52: 20.6,
    53: 19.8,
    54: 21.6,
    78: 17.5,
    79: 16.6,
    80: 15.5,
    81: 19.6,
    82: 20.2,
    92: 18.6,
}

default_colors = {
    1: "white", # hydrogen
    8: "red", # oxygen
}

def plot_sphere_surface(origin: tuple[int, int, int]=(0, 0, 0), radius: int=1, color: str="red"):
    '''
    Plots on an existing ipyvolume figure the surface of a sphere. By default
    the sphere is located at the origin (0, 0, 0) with a radius of 1 and color
    "red".
    '''
    x_origin, y_origin, z_origin = origin
    step = 0.1
    gridx, gridy = np.ix_(np.arange(0, np.pi + step, step), np.arange(0, 2 * np.pi + step, step))

    @np.vectorize
    def sphere_surface(phi: float, theta: float):
        x = x_origin + radius * np.sin(phi) * np.cos(theta)
        y = y_origin + radius * np.sin(phi) * np.sin(theta)
        z = z_origin + radius * np.cos(phi)
        return (x, y, z)

    x, y, z = np.array(list(sphere_surface(gridx, gridy)))
    ipv.plot_surface(x, z, y, color=color)

def plot_atoms(cube: Cube, sizes: dict[int, int]=vanderwaals, colors: dict[int, str]=default_colors):
    '''
    Plots the atoms from a provided Cube object using the sizes and colors in
    the provided dicts. The keys are the atomic number of the atoms in the cell.
    '''
    default_color = "red"
    default_size = 10
    for atom in range(len(cube.atoms)):
        position = cube.atoms.get_scaled_positions()[atom]
        number = cube.atoms.get_atomic_numbers()[atom]
        x, z, y = tuple(p * cube.data3D.shape[idx] / Bohr for idx, p in enumerate(position))
        plot_sphere_surface((x, y, z), sizes[number] or default_size, colors[number] or default_color)