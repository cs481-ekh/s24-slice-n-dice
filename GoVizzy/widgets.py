'''This File is for widgets used by GoVizzy
    Input form: widget for uploading a .cube file
    Options: Widget containing options for customization of output.
    Documentation for widget library: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#file-upload
'''
from IPython.display import display
from ipywidgets import Layout, Button, Box, Textarea, Label, FloatSlider

# Input form
# Layout for Input form
form_item_layout = Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'
)

test_slider = FloatSlider(
    value=0,
    min=0,
    max=10,
    step=0.1,
    description='Example slider!',
    readout=True,
    readout_format='.1f'
)

# Input form items
form_items = [

    Box([Label(value='Path to .cube file'), 
         Textarea()], layout=form_item_layout),
    Button(description='Submit', layout=Layout(flex='1 1 0%', width='auto')),
    test_slider,
    
]

# Create the input form box
form = Box(form_items, layout=Layout(
    display='flex',
    flex_flow='row',
    border='solid 2px',
    align_items='stretch',
    width='50%'
))
form, test_slider
