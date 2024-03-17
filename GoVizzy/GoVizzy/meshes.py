from UI.widgets import color
from cube_viskit import Cube
import ipywidgets as widgets
import ipyvolume as ipv
import numpy as np
from IPython.display import display

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