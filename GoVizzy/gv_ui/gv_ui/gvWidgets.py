'''This File is for widgets used by GoVizzy
    Input form: widget for uploading a .cube file
    Documentation for widget library: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#file-upload
'''
from IPython.display import display
from ipywidgets import Layout, Button, Box, Textarea, Label, ColorPicker, FloatSlider, Checkbox, link, BoundedFloatText, IntSlider, Dropdown
from ipyvolume.widgets import Mesh, Scatter
import numpy as np

# Input form
# Layout for Input form
form_item_layout = Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'
)


slice_x_slider = IntSlider(
    value=0,
    min=0,
    max=119,
    step=1,
    description='X Pos',
    readout=True,
    readout_format='d'
)

slice_y_slider = IntSlider(
    value=0,
    min=0,
    max=119,
    step=1,
    description='Y Pos',
    readout=True,
    readout_format='d'
)

slice_z_slider = IntSlider(
    value=0,
    min=0,
    max=119,
    step=1,
    description='Z Pos',
    readout=True,
    readout_format='d'
)

slice_x_check = Checkbox(
    value=False,
    description='X Toggle',
    disabled=False,
    indent=True
)

slice_y_check = Checkbox(
    value=False,
    description='Y Toggle',
    disabled=False,
    indent=True
)

slice_z_check = Checkbox(
    value=False,
    description='Z Toggle',
    disabled=False,
    indent=True
)

slice_color = Dropdown(
    options=['Grays', 'Reds', 'Oranges', 'Greens', 'Blues', 'Purples'],
    description='Slice Color Scheme',
    disabled=False,
    indent=True
)

bond_visibility_toggle = Checkbox(
    value=True,
    description='Bond Visibility',
    disabled=False,
    indent=True
)

bond_color_picker = ColorPicker(
    value="black",
    description="Bond Color"
)

bond_scale_slider = BoundedFloatText(
        value=3,
        min=0,
        max=10,
        step=0.01,
        description="Bond Scale",
        continuous_update=False
)

def mesh_visibility_toggle(mesh: Mesh, description: str="Atom"):
    """
    Returns an ipywidget.Checkbox with the provided description and links the
    value to the provided mesh visibility.
    """

    toggle = Checkbox(value=True, description=description)
    link((toggle, 'value'), (mesh, 'visible'))
    return toggle

color = ColorPicker(concise=True, value='white', description='Color', disabled=False, layout=Layout(flex='1 1 0%', width='auto'))

def atom_color_picker(atom: Mesh, description: str="Color"):
    """
    Returns an ipywidget.ColorPicker with the provided description and links the
    value to the provided mesh color.
    """

    picker = ColorPicker(value=str(atom.color), description=description)
    link((picker, 'value'), (atom, 'color'))
    return picker


def scale_atom_mesh(atom: Mesh, points: tuple[list, list, list], origin: tuple[float, float, float], scale: float):
    """
    Scales the size of the original atom size by the scaling factor. Sets the
    scaled values to the provided atom.
    """

    x, y, z = points
    origin_x, origin_y, origin_z = origin
    scaled_x = (x - origin_x) * scale + origin_x
    scaled_y = (y - origin_y) * scale + origin_y
    scaled_z = (z - origin_z) * scale + origin_z
    atom.x, atom.y, atom.z = scaled_x, scaled_y, scaled_z

def atom_scale_slider(atom: Mesh, description: str="Scale"):
    """
    Returns an ipywidget.BoundedFloatText with the provided description and
    links the value to a function which adjusts the scale of the atom.
    """

    slider = BoundedFloatText(
        value=1,
        min=0,
        max=10,
        step=0.01,
        description=description,
        continuous_update=False
    )
    points = (list(atom.x), list(atom.y), list(atom.z))
    origin = (np.mean(atom.x), np.mean(atom.y), np.mean(atom.z))
    slider.observe(lambda change: scale_atom_mesh(atom, points, origin, change.new), 'value')
    return slider

# Input form items
form_items = [

    Box([Label(value='Path to .cube file'),
         Textarea()], layout=form_item_layout),
    color,
    Button(description='Submit', layout=Layout(flex='1 1 0%', width='auto')),
    slice_x_slider,
]

# Create the input form box
form = Box(form_items, layout=Layout(
    display='flex',
    flex_flow='row',
    border='solid 2px',
    align_items='stretch',
    width='50%'
))

form, color, slice_x_slider, slice_y_slider, slice_z_slider, slice_x_check, slice_y_check, slice_z_check, slice_color, bond_scale_slider, bond_color_picker, bond_visibility_toggle
