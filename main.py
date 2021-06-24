from bokeh.plotting import figure, curdoc
from bokeh.layouts import layout
#from bokeh.models.widgets import Tabs, Panel

import app_cockpit
import platform_stat_dash

curdoc().theme = 'dark_minimal'

#tab1 = Panel(child=platform_stat_dash.layout1, title="Platform Statistic Dashboard")
#tab2 = Panel(child=app_cockpit.layout2, title="Application Cockpit")
#tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(platform_stat_dash.layout1)

