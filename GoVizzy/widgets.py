'''This File is for widgets used by GoVizzy
    Input form: widget for uploading a .cube file
    Documentation for widget library: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#file-upload
'''
from IPython.display import display
from ipywidgets import Layout, Button, Box, Textarea, Label, ColorPicker, FloatSlider

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
    description='X slice position',
    readout=True,
    readout_format='.1f'
)

slice_y_slider = FloatSlider(
    value=0,
    min=0,
    max=120,
    step=0.1,
    description='Y slice position',
    readout=True,
    readout_format='.1f'
)

slice_z_slider = FloatSlider(
    value=0,
    min=0,
    max=120,
    step=0.1,
    description='Z slice position',
    readout=True,
    readout_format='.1f'
)

color = ColorPicker(concise=True, value='blue', description='Color', disabled=False, layout=Layout(flex='1 1 0%', width='auto'))


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

form, color, slice_x_slider, slice_y_slider, slice_z_slider
