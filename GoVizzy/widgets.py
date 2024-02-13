
from IPython.display import display
import ipywidgets as widgets
from widgets import Layout, Button, Box, Textarea, Label

form_item_layout = Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'
)

form_items = [

    Box([Label(value='Path to .cube file'), 
         Textarea()], layout=form_item_layout),
    Button(description='Submit', layout=Layout(flex='1 1 0%', width='auto')),
    
]

form = Box(form_items, layout=Layout(
    display='flex',
    flex_flow='row',
    border='solid 2px',
    align_items='stretch',
    width='50%'
))
form

display(form)