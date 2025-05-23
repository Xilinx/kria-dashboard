# Copyright 2021 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This version of kria-dashboard has been tested with Bokeh 3.5.1
# This version of kria-dashboard is not backward compatible with Bokeh 2.4.2


from bokeh.plotting import figure, curdoc
from bokeh.layouts import layout, row, column
from bokeh.models import TabPanel, Tabs
from bokeh.models import (
    ColumnDataSource,
    DataTable,
    TableColumn,
)
from bokeh.models import Button, Div, Range1d
from bokeh.models import HoverTool
from bokeh.models import TextInput
from bokeh.models import Div
from bokeh.driving import linear




from xlnx_platformstats import xlnx_platformstats

xlnx_platformstats.init()

bg_color = "#15191C"
text_color = "#E0E0E0"

def list_popleft(my_list):
    #return my_list[1:]
    # Check if the list is not empty
    if my_list:
        # Remove and return the first element
        return my_list.pop(0)
    else:
        raise IndexError("pop from empty list")


##################################################
##### Platform Stat Tab ##########################
##################################################

sample_size = 60
sample_size_actual = 60
interval = 1
x = [0] * sample_size
color_list = [
    "darkseagreen",
    "steelblue",
    "indianred",
    "chocolate",
    "mediumpurple",
    "rosybrown",
    "gold",
    "mediumaquamarine",
]


def clear_min_max():
    max_volt[:] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    max_temp[:] = [0, 0, 0]
    min_volt[:] = [7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
    min_temp[:] = [200, 200, 200]
    global average_cpu, average_cpu_sample_size
    average_cpu = 0
    average_cpu_sample_size = 0


cpu_labels = [
    "A-53_Core_0",
    "A-53_Core_1",
    "A-53_Core_2",
    "A-53_Core_3",
]
cpu_data = {
    "A-53_Core_0": [0.0] * sample_size,
    "A-53_Core_1": [0.0] * sample_size,
    "A-53_Core_2": [0.0] * sample_size,
    "A-53_Core_3": [0.0] * sample_size,
}
volt_labels = [
    "VCC_PSPLL",
    "PL_VCCINT",
    "VOLT_DDRS",
    "VCC_PSINTFP",
    "VCC_PS_FPD",
    "PS_IO_BANK_500",
    "VCC_PS_GTR",
    "VTT_PS_GTR",
    "Total_Volt",
]
volt_data = {
    "VCC_PSPLL": [0] * sample_size,
    "PL_VCCINT": [0] * sample_size,
    "VOLT_DDRS": [0] * sample_size,
    "VCC_PSINTFP": [0] * sample_size,
    "VCC_PS_FPD": [0] * sample_size,
    "PS_IO_BANK_500": [0] * sample_size,
    "VCC_PS_GTR": [0] * sample_size,
    "VTT_PS_GTR": [0] * sample_size,
    "Total_Volt": [0] * sample_size,
}
temp_labels = [
    "LPD_TEMP",
    "FPD_TEMP",
    "PL_TEMP",
]
temp_data = {
    "LPD_TEMP": [0.0] * sample_size,
    "FPD_TEMP": [0.0] * sample_size,
    "PL_TEMP": [0.0] * sample_size,
}

# note that if a queue is not getting appended every sample, remove it from data structure, or
# popping the queue when updating sample size will not work!
mem_labels = [
    # "MemTotal",
    "MemFree",
    # "MemAvailable",
    # "SwapTotal",
    # "SwapFree",
    # "CmaTotal",
    # "CmaFree",
]
mem_data = {
    # "MemTotal": [0] * sample_size,
    "MemFree": [0] * sample_size,
    # "MemAvailable": [0] * sample_size,
    # "SwapTotal": [0] * sample_size,
    # "SwapFree": [0] * sample_size,
    # "CmaTotal": [0] * sample_size,
    # "CmaFree": [0] * sample_size,
}

current_data = [0] * sample_size
power_data = [0] * sample_size

# title
title1 = Div(
    text="""<h1 style="color :"""
    + text_color
    + """; text-align :center">Kria&trade; SOM: Hardware Platform Statistics</h1>""",
    width=550,
)

# average cpu display
average_cpu = 0.0
average_cpu_sample_size = 0
average_cpu_display = Div(text=str(average_cpu), width=600)

# CPU frequency display
cpu_freq_text = """<h3 style="color :""" + text_color + """;">CPU Frequencies </h3>"""
cpu_freq = [0, 0, 0, 0]
cpu_freq_display = Div(text=cpu_freq_text, width=400)

# CPU line plot
cpu_plot = figure(width=800, height=300, title="CPU Utilization %")
cpu_ds = [0, 0, 0, 0]
for i in range(len(cpu_labels)):
    cpu_ds[i] = (
        cpu_plot.line(
            x,
            cpu_data[cpu_labels[i]],
            line_width=2,
            color=color_list[i],
            legend_label=cpu_labels[i],
        )
    ).data_source
cpu_plot.legend.click_policy = "hide"

# current line plot
current_plot = figure(width=500, height=300, title="Total SOM Current in mA")
current_ds = (
    current_plot.line(
        x, current_data, line_width=2, color=color_list[0], legend_label="Current"
    )
).data_source
current_plot.legend.click_policy = "hide"

# power line plot
power_plot = figure(width=500, height=300, title="Total SOM Power in W")
power_ds = (
    power_plot.line(
        x, power_data, line_width=2, color=color_list[0], legend_label="Power"
    )
).data_source
power_plot.legend.click_policy = "hide"

# temperature line plot
temp_plot = figure(width=500, height=300, title="Temperature in Celsius")
temp_ds = [0, 0, 0, 0]
temp_ds[0] = (
    temp_plot.line(
        x,
        temp_data[temp_labels[0]],
        line_width=2,
        color=color_list[0],
        legend_label=temp_labels[0],
    )
).data_source
temp_plot.legend.click_policy = "hide"

# table of min/max for temperature
max_temp = [0.0, 0.0, 0.0]
min_temp = [200.0, 200.0, 200.0]
min_max_temp = dict(temp_labels=temp_labels, max_temp=max_temp, min_temp=min_temp)
min_max_temp_source = ColumnDataSource(min_max_temp)
min_max_temp_column = [
    TableColumn(field="temp_labels", title="Temperature"),
    TableColumn(field="max_temp", title="Max"),
    TableColumn(field="min_temp", title="Min"),
]

temp_data_table = DataTable(
    source=min_max_temp_source,
    columns=min_max_temp_column,
    index_position=None,
    width=400,
    height=200,
    background=bg_color,
    css_classes=["custom_table"],
)

# table of min/max for voltages
max_volt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
min_volt = [7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
min_max_volt = dict(volt_labels=volt_labels, max_volt=max_volt, min_volt=min_volt)
min_max_volt_source = ColumnDataSource(min_max_volt)
min_max_volt_column = [
    TableColumn(field="volt_labels", title="Voltage"),
    TableColumn(field="max_volt", title="Max"),
    TableColumn(field="min_volt", title="Min"),
]

volt_data_table = DataTable(
    source=min_max_volt_source,
    columns=min_max_volt_column,
    index_position=None,
    width=400,
    height=200,
    background=bg_color,
    css_classes=["custom_table"],
)

# memory line plot
mem_plot = figure(width=800, height=300, title="Total Free Memory in kB")
mem_ds = (
    mem_plot.line(
        x,
        mem_data["MemFree"],
        line_width=2,
        color=color_list[0],
        legend_label="MemFree",
    )
).data_source
mem_plot.legend.click_policy = "hide"

# memory bar plot
mem_bar_label = ["MemUsed", "SwapUsed", "CMAUsed"]
mem_bar_total = [0, 0, 0]
mem_bar_used = [0, 0, 0]
mem_bar_available = [0, 0, 0]
mem_bar_percent = [0.0, 0.0, 0.0]
mem_bar_dict = dict(
    mem_bar_label=mem_bar_label,
    mem_bar_total=mem_bar_total,
    mem_bar_used=mem_bar_used,
    mem_bar_percent=mem_bar_percent,
    mem_bar_available=mem_bar_available,
)
mem_bar_source = ColumnDataSource(mem_bar_dict)
mem_plot_hbar = figure(
    y_range=mem_bar_label,
    x_range=[0, 100],
    width=800,
    height=300,
    title="Memory Usage in %",
)
mem_plot_hbar.xaxis.axis_label = "%Used"
mem_percent_ds = (
    mem_plot_hbar.hbar(
        y="mem_bar_label",
        right="mem_bar_percent",
        tags=mem_bar_label,
        source=mem_bar_source,
        height=0.5,
        fill_color="steelblue",
        hatch_pattern="vertical_line",
        hatch_weight=2,
        line_width=0,
    )
).data_source
hover = HoverTool(
    tooltips=[("Total in kB:", "@mem_bar_total"), ("Used in kB:", "@mem_bar_used")]
)
mem_plot_hbar.add_tools(hover)

# reset button
reset_button = Button(
    label="Reset Min/Max and Averages", width=200, button_type="primary"
)
reset_button.on_click(clear_min_max)


# sample interval
def update_interval(attr, old, new):
    global interval
    interval = max(float(new), 0.5)
    global input_interval
    input_interval.value = str(interval)
    global callback
    curdoc().remove_periodic_callback(callback)
    callback = curdoc().add_periodic_callback(update, interval * 1000)


input_interval = TextInput(
    value=str(interval),
    title="input interval in seconds (minimal 0.5s):",
    css_classes=["custom_textinput"],
    width=100,
)
input_interval.on_change("value", update_interval)


# sample size
def update_sample_size(attr, old, new):
    global sample_size, sample_size_actual
    new_sample_size = int(new)
    if new_sample_size < sample_size_actual:
        excess = sample_size_actual - new_sample_size
        while excess > 0:
            list_popleft(x)
            for j in range(len(cpu_labels)):
                list_popleft(cpu_data[cpu_labels[j]])
            for j in range(len(volt_labels)):
                list_popleft(volt_data[volt_labels[j]])
            for j in range(len(temp_labels)):
                list_popleft(temp_data[temp_labels[j]])
            for j in range(len(mem_labels)):
                list_popleft(mem_data[mem_labels[j]])
            excess = excess - 1
        sample_size_actual = new_sample_size
    sample_size = new_sample_size


input_sample_size = TextInput(
    value=str(sample_size),
    title="Sample Size:",
    css_classes=["custom_textinput"],
    width=100,
)
input_sample_size.on_change("value", update_sample_size)

time = 0

# default_data_range = cpu_plot.y_range

cpu_plot.y_range = Range1d(0, 100)

mem_result1 = (
    xlnx_platformstats.get_ram_memory_utilization()
)  # Returns list [return_val, MemTotal, MemFree, MemAvailable]
mem_plot.y_range = Range1d(0, mem_result1[1])  # get_mem("MemTotal"))
power_plot.y_range = Range1d(0, 6)
current_plot.y_range = Range1d(0, 1000)
temp_plot.y_range = Range1d(0, 100)


# # dynamic scaling:
# def update_scaling(attr, old, new):
#     if new == [0]:
#         cpu_plot.y_range = default_data_range
#         cpu_plot.title.text = "name 1"
#     else:
#         cpu_plot.y_range = Range1d(0, 50)
#         cpu_plot.title.text = "name 2"
#
# checkbox_labels = ["Enable Dynamic Y-axis Scaling"]
# checkbox_group = CheckboxGroup(labels=checkbox_labels, active=[], css_classes=['custom_textinput'],)
# checkbox_group.on_change('active', update_scaling)


@linear()
def update(step):
    global time
    global sample_size_actual
    time = time + interval
    if sample_size_actual >= sample_size:
        list_popleft(x)
    x.append(time)

    read = xlnx_platformstats.get_cpu_utilization()

    average_cpu_x = 0
    for j in range(len(cpu_labels)):
        if sample_size_actual >= sample_size:
            list_popleft(cpu_data[cpu_labels[j]])
        cpu_data_read = read[j]
        cpu_data[cpu_labels[j]].append(cpu_data_read)
        cpu_ds[j].trigger("data", x, cpu_data[cpu_labels[j]])
        average_cpu_x = average_cpu_x + cpu_data_read

    # average CPU usage
    global average_cpu_sample_size, average_cpu
    average_cpu = average_cpu * average_cpu_sample_size
    average_cpu_sample_size = average_cpu_sample_size + 1
    average_cpu = (average_cpu + (average_cpu_x / 4)) / average_cpu_sample_size

    text = (
        """<h2 style="color :"""
        + text_color
        + """;">"""
        + "&nbsp; &nbsp; Average CPU utilization over last "
        + str(average_cpu_sample_size)
        + " samples is "
        + str(round(average_cpu, 2))
        + """%</h2>"""
    )
    average_cpu_display.text = text

    # CPU frequency
    cpu_freq = []

    for j in range(4):
        cpu_freq.append(
            str(xlnx_platformstats.get_cpu_frequency(j)[1])
        )  # //Returns list [return_val, cpu_freq]
        # cpu_freq.append(open('/sys/devices/system/cpu/cpu' + str(j) + '/cpufreq/cpuinfo_cur_freq', 'r').read())

    cpu_freq_display.text = (
        cpu_freq_text
        + """<p style="color :"""
        + text_color
        + """;">&nbsp; &nbsp;CPU0:"""
        + cpu_freq[0]
        + "MHz<br>&nbsp; &nbsp;CPU1:"
        + cpu_freq[1]
        + "MHz<br>&nbsp; &nbsp;CPU2:"
        + cpu_freq[2]
        + "MHz<br>&nbsp; &nbsp;CPU3:"
        + cpu_freq[3]
        + "MHz"
    )

    volts = []
    volts = (
        xlnx_platformstats.get_voltages()
    )  # Returns list [return_val, VCC_PSPLL, PL_VCCINT, VOLT_DDRS, VCC_PSINTFP, VCC_PS    _FPD, PS_IO_BANK_500, VCC_PS_GTR, VTT_PS_GTR, total_voltage]
    volts.pop(0)

    for j in range(len(volt_labels)):
        if sample_size_actual >= sample_size:
            list_popleft(volt_data[volt_labels[j]])
        volt_read = int(volts[j])
        volt_data[volt_labels[j]].append(volt_read)
        if (volt_read < min_volt[j]) or (volt_read > max_volt[j]):
            min_volt[j] = min(min_volt[j], int(volts[j]))
            max_volt[j] = max(max_volt[j], int(volts[j]))
            volt_data_table.source.trigger(
                "data", volt_data_table.source, volt_data_table.source
            )

    temperatures = []
    temperatures = (
        xlnx_platformstats.get_temperatures()
    )  # Returns list [return_val, LPD_TEMP, FPD_TEMP, PL_TEMP]
    temperatures.pop(0)
    for j in range(len(temp_labels)):
        if sample_size_actual >= sample_size:
            list_popleft(temp_data[temp_labels[j]])
        temperature_read = (float(temperatures[j])) / 1000
        temp_data[temp_labels[j]].append(temperature_read)
        if (temperature_read < min_temp[j]) or (temperature_read > max_temp[j]):
            min_temp[j] = min(min_temp[j], temperature_read)
            max_temp[j] = max(max_temp[j], temperature_read)
            temp_data_table.source.trigger(
                "data", temp_data_table.source, temp_data_table.source
            )
    temp_ds[0].trigger("data", x, temp_data[temp_labels[0]])

    ina260_current = xlnx_platformstats.get_current()[
        1
    ]  # Returns list [return_val, total_current

    if sample_size_actual >= sample_size:
        list_popleft(current_data)
    current_data.append(int(ina260_current))
    current_ds.trigger("data", x, current_data)

    ina260_power = (
        xlnx_platformstats.get_power()[1] / 1000000
    )  # Returns list [return_val, total_power]
    if sample_size_actual >= sample_size:
        list_popleft(power_data)
    power_data.append(ina260_power)
    power_ds.trigger("data", x, power_data)

    # Mem line chart
    mem_result1 = (
        xlnx_platformstats.get_ram_memory_utilization()
    )  # Returns list [return_val, MemTotal, MemFree, MemAvailable]
    mem_result2 = (
        xlnx_platformstats.get_swap_memory_utilization()
    )  # Returns list [return_val, SwapTotal, SwapFree]
    mem_result3 = (
        xlnx_platformstats.get_cma_utilization()
    )  # Returns list [return_val, CmaTotal, CmaFree]
    mem_num = mem_result1[2]  # get_mem("MemFree")
    if sample_size_actual >= sample_size:
        list_popleft(mem_data["MemFree"])
    mem_data["MemFree"].append(mem_num)
    mem_ds.trigger("data", x, mem_data["MemFree"])

    # Memory usage Horizontal bar chart
    mem_bar_total[0] = mem_result1[1]  # get_mem('MemTotal')
    mem_bar_available[0] = mem_result1[3]  # get_mem('MemAvailable')
    mem_bar_used[0] = mem_bar_total[0] - mem_bar_available[0]
    mem_bar_percent[0] = 100 * mem_bar_used[0] / max(mem_bar_total[0], 1)
    mem_bar_total[1] = mem_result2[1]  # get_mem('SwapTotal')
    mem_bar_available[1] = mem_result2[2]  # get_mem('SwapFree')
    mem_bar_used[1] = mem_bar_total[1] - mem_bar_available[1]
    mem_bar_percent[1] = 100 * mem_bar_used[1] / max(mem_bar_total[1], 1)
    mem_bar_total[2] = mem_result3[1]  # get_mem('CmaTotal')
    mem_bar_available[2] = mem_result3[2]  # get_mem('CmaFree')
    mem_bar_used[2] = mem_bar_total[2] - mem_bar_available[2]
    mem_bar_percent[2] = 100 * mem_bar_used[2] / max(mem_bar_total[2], 1)
    mem_percent_ds.trigger("data", mem_bar_label, mem_bar_percent)

    if sample_size_actual < sample_size:
        sample_size_actual = sample_size_actual + 1


# margin:  Margin-Top, Margin-Right, Margin-Bottom and Margin-Left
user_interface = column(
    reset_button,
    input_sample_size,
    input_interval,  # checkbox_group,
    background=bg_color,
    margin=(50, 50, 50, 100),
)
cpu_freq_block = column(cpu_freq_display, background=bg_color, margin=(0, 0, 0, 100))
layout1 = layout(
    column(
        row(title1, align="center"),
        average_cpu_display,
        row(cpu_plot, user_interface, cpu_freq_block, background=bg_color),
        row(mem_plot, mem_plot_hbar, background=bg_color),
        row(power_plot, current_plot, temp_plot, background=bg_color),
        row(volt_data_table, temp_data_table, background=bg_color),
        background=bg_color,
    )
)

# Add a periodic callback to be run every 1000 milliseconds
callback = curdoc().add_periodic_callback(update, interval * 1000)

##################################################
##### Group Tabs        ##########################
##################################################

curdoc().theme = "dark_minimal"
tab1 = TabPanel(child=layout1, title="Platform Statistic Dashboard")
tabs = Tabs(tabs=[tab1])
curdoc().add_root(tabs)
