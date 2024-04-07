'''This File is for widgets used by GoVizzy
    Input form: widget for uploading a .cube file
    Documentation for widget library: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#file-upload
'''
from IPython.display import display
from ipywidgets import Layout, Button, Box, Textarea, Label, ColorPicker, FloatSlider, Checkbox, link
from ipyvolume.widgets import Mesh

# Input form
# Layout for Input form
form_item_layout = Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'
)


slice_x_slider = FloatSlider(
    value=0,
    min=0,
    max=120,
    step=0.1,
    description='X Pos',
    readout=True,
    readout_format='.1f'
)

slice_y_slider = FloatSlider(
    value=0,
    min=0,
    max=120,
    step=0.1,
    description='Y Pos',
    readout=True,
    readout_format='.1f'
)

slice_z_slider = FloatSlider(
    value=0,
    min=0,
    max=120,
    step=0.1,
    description='Z Pos',
    readout=True,
    readout_format='.1f'
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

def mesh_visibility_toggle(mesh: Mesh, description: str="Atom"):
    toggle = Checkbox(value=True, description=description)
    link((toggle, 'value'), (mesh, 'visible'))
    return toggle

color = ColorPicker(concise=True, value='white', description='Color', disabled=False, layout=Layout(flex='1 1 0%', width='auto'))


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

form, color, slice_x_slider, slice_y_slider, slice_z_slider, slice_x_check, slice_y_check, slice_z_check
