'''This File is for widgets used by GoVizzy
    Input form: widget for uploading a .cube file
    Documentation for widget library: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#file-upload
'''
from IPython.display import display
from ipywidgets import Layout, Button, Box, Textarea, Label

# Layout for Input form
form_item_layout = Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'
)

# Input form items
form_items = [

    Box([Label(value='Path to .cube file'), 
         Textarea()], layout=form_item_layout),
    Button(description='Submit', layout=Layout(flex='1 1 0%', width='auto')),
    
]

# Create the input form box
form = Box(form_items, layout=Layout(
    display='flex',
    flex_flow='row',
    border='solid 2px',
    align_items='stretch',
    width='50%'
))
form
