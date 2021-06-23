from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import random
import psutil
from bokeh.models.annotations import Title
from collections import deque
from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter
from bokeh.io import output_notebook

output_notebook()
from bokeh.events import ButtonClick
from bokeh.models import Button, Paragraph, Div
from bokeh.themes import built_in_themes
import subprocess
from bokeh.models import HoverTool
from bokeh.models import TextInput

from bokeh.layouts import layout
from bokeh.models.widgets import Tabs, Panel

# import panel as pn
# pn.extension('echarts')


import global_var
import app_cockpit
import platform_stat_dash

curdoc().theme = 'dark_minimal'

tab1 = Panel(child=platform_stat_dash.layout1, title="Platform Statistic Dashboard")
tab2 = Panel(child=app_cockpit.layout2, title="Application Cockpit")
tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)

# Add a periodic callback to be run every 1000 milliseconds
callback = curdoc().add_periodic_callback(platform_stat_dash.update, platform_stat_dash.interval * 1000)
