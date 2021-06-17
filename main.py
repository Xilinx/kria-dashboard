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


def get_mem(memtype):
    mem_val = int(
        ''.join(filter(str.isdigit, str(subprocess.run(['/bin/grep', memtype, '/proc/meminfo'], capture_output=True)))))
    return mem_val


def clear_min_max():
    max_volt[:] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    max_temp[:] = [0, 0, 0]
    min_volt[:] = [7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
    min_temp[:] = [200, 200, 200]
    global average_cpu, average_cpu_sample_size
    average_cpu = 0
    average_cpu_sample_size = 0


curdoc().theme = 'dark_minimal'
bg_color = '#15191C'
text_color = '#E0E0E0'
sample_size = 60
sample_size_actual = 60
interval = 1
x = deque([0] * sample_size)
color_list = ["darkseagreen", "steelblue", "indianred", "chocolate", "mediumpurple", "rosybrown", "gold",
              "mediumaquamarine"]

cpu_labels = [
    "A-53_Core_0",
    "A-53_Core_1",
    "A-53_Core_2",
    "A-53_Core_3",
]
cpu_data = {
    'A-53_Core_0': deque([0.0] * sample_size),
    'A-53_Core_1': deque([0.0] * sample_size),
    'A-53_Core_2': deque([0.0] * sample_size),
    'A-53_Core_3': deque([0.0] * sample_size),
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
    "VCC_PSPLL": deque([0] * sample_size),
    "PL_VCCINT": deque([0] * sample_size),
    "VOLT_DDRS": deque([0] * sample_size),
    "VCC_PSINTFP": deque([0] * sample_size),
    "VCC_PS_FPD": deque([0] * sample_size),
    "PS_IO_BANK_500": deque([0] * sample_size),
    "VCC_PS_GTR": deque([0] * sample_size),
    "VTT_PS_GTR": deque([0] * sample_size),
    "Total_Volt": deque([0] * sample_size),
}
temp_labels = [
    "FPD_TEMP",
    "LPD_TEMP",
    "PL_TEMP",
]
temp_data = {
    "FPD_TEMP": deque([0.0] * sample_size),
    "LPD_TEMP": deque([0.0] * sample_size),
    "PL_TEMP": deque([0.0] * sample_size),
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
    # "MemTotal": deque([0] * sample_size),
    "MemFree": deque([0] * sample_size),
    # "MemAvailable": deque([0] * sample_size),
    # "SwapTotal": deque([0] * sample_size),
    # "SwapFree": deque([0] * sample_size),
    # "CmaTotal": deque([0] * sample_size),
    # "CmaFree": deque([0] * sample_size),
}

current_data = deque([0] * sample_size)
power_data = deque([0] * sample_size)

# title
title = Div(
    text="""<h1 style="color :""" + text_color + """; text-align :center">Kria Zynq MPSoc Platform Statistic</h1>""",
    width=450)

# average cpu display
average_cpu = 0.0
average_cpu_sample_size = 0
average_cpu_display = Div(text=str(average_cpu), width=600)

# CPU line plot
cpu_plot = figure(plot_width=800, plot_height=300, title='CPU Utilization %')
# cpu_plot.yaxis.axis_label = 'CPU Usage in %'
cpu_ds = [0, 0, 0, 0]
for i in range(len(cpu_labels)):
    cpu_ds[i] = (cpu_plot.line(x, cpu_data[cpu_labels[i]], line_width=2,
                               color=color_list[i], legend_label=cpu_labels[i])).data_source
cpu_plot.legend.click_policy = "hide"

# current line plot
current_plot = figure(plot_width=500, plot_height=300, title='Current in mA')
# current_plot.yaxis.axis_label = 'Current'
current_ds = (current_plot.line(x, current_data, line_width=2,
                                color=color_list[0], legend_label="Current")).data_source
current_plot.legend.click_policy = "hide"

# power line plot
power_plot = figure(plot_width=500, plot_height=300, title='Total Power in W')
# power_plot.yaxis.axis_label = 'Power'
power_ds = (power_plot.line(x, power_data, line_width=2,
                            color=color_list[0], legend_label="Power")).data_source
power_plot.legend.click_policy = "hide"

# temperature line plot
temp_plot = figure(plot_width=500, plot_height=300, title='Temperature in C')
temp_ds = [0, 0, 0, 0]
temp_ds[0] = (temp_plot.line(x, temp_data[temp_labels[0]], line_width=2,
                             color=color_list[0], legend_label=temp_labels[0])).data_source
temp_plot.legend.click_policy = "hide"

# table of min/max for temperature
max_temp = [0.0, 0.0, 0.0]
min_temp = [200.0, 200.0, 200.0]
min_max_temp = dict(temp_labels=temp_labels, max_temp=max_temp, min_temp=min_temp)
min_max_temp_source = ColumnDataSource(min_max_temp)
min_max_temp_column = [
    TableColumn(field="temp_labels", title="Temperature"),
    TableColumn(field="max_temp", title="Max"),
    TableColumn(field="min_temp", title="Min")
]

temp_data_table = DataTable(source=min_max_temp_source, columns=min_max_temp_column, index_position=None,
                            width=400, height=200, background=bg_color, css_classes=['custom_table'])

# table of min/max for voltages
max_volt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
min_volt = [7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
min_max_volt = dict(volt_labels=volt_labels, max_volt=max_volt, min_volt=min_volt)
min_max_volt_source = ColumnDataSource(min_max_volt)
min_max_volt_column = [
    TableColumn(field="volt_labels", title="Voltage"),
    TableColumn(field="max_volt", title="Max"),
    TableColumn(field="min_volt", title="Min")
]

volt_data_table = DataTable(source=min_max_volt_source, columns=min_max_volt_column, index_position=None,
                            width=400, height=200, background=bg_color, css_classes=['custom_table'])

# memory line plot
mem_plot = figure(plot_width=800, plot_height=300, title='Memory Usage in kB')
mem_ds = (mem_plot.line(x, mem_data["MemFree"], line_width=2,
                        color=color_list[0], legend_label="MemFree")).data_source
mem_plot.legend.click_policy = "hide"

# memory bar plot
mem_bar_label = ['MemUsed', 'SwapUsed', 'CMAUsed']
mem_bar_total = [0, 0, 0]
mem_bar_used = [0, 0, 0]
mem_bar_available = [0, 0, 0]
mem_bar_percent = [0.0, 0.0, 0.0]
mem_bar_dict = dict(mem_bar_label=mem_bar_label, mem_bar_total=mem_bar_total,
                    mem_bar_used=mem_bar_used, mem_bar_percent=mem_bar_percent,
                    mem_bar_available=mem_bar_available)
mem_bar_source = ColumnDataSource(mem_bar_dict)
mem_plot_hbar = figure(y_range=mem_bar_label, x_range=[0, 100], plot_width=800, plot_height=300,
                       title='Memory Usage in %')
mem_plot_hbar.xaxis.axis_label = '%Used'
mem_percent_ds = (mem_plot_hbar.hbar(y='mem_bar_label', right='mem_bar_percent',
                                     tags=mem_bar_label, source=mem_bar_source,
                                     height=.5, fill_color='steelblue',
                                     hatch_pattern='vertical_line', hatch_weight=2, line_width=0)).data_source
hover = HoverTool(tooltips=[("Total in kB:", "@mem_bar_total"), ("Used in kB:", "@mem_bar_used")])
mem_plot_hbar.add_tools(hover)

# reset button
reset_button = Button(label="Reset Min/Max and Averages", width=200, button_type='primary')
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


input_interval = TextInput(value=str(interval), title="input interval in seconds (minimal 0.5s):",
                           css_classes=['custom_textinput'], width = 100)
input_interval.on_change('value', update_interval)


# sample size
def update_sample_size(attr, old, new):
    global sample_size, sample_size_actual
    new_sample_size = int(new)
    if new_sample_size < sample_size_actual:
        excess = sample_size_actual - new_sample_size
        while excess > 0:
            x.popleft();
            for j in range(len(cpu_labels)):
                cpu_data[cpu_labels[j]].popleft()
            for j in range(len(volt_labels)):
                volt_data[volt_labels[j]].popleft()
            for j in range(len(temp_labels)):
                temp_data[temp_labels[j]].popleft()
            for j in range(len(mem_labels)):
                mem_data[mem_labels[j]].popleft()
            excess = excess - 1
        sample_size_actual = new_sample_size
    sample_size = new_sample_size
    print("samplesize", sample_size)
    print("samplesizeactual", sample_size_actual)


input_sample_size = TextInput(value=str(sample_size), title="Sample Size:",
                              css_classes=['custom_textinput'], width = 100)
input_sample_size.on_change('value', update_sample_size)

time = 0

@linear()
def update(step):
    global time
    global sample_size_actual
    time = time + interval
    if sample_size_actual >= sample_size:
        x.popleft()
    x.append(time)

    read = psutil.cpu_percent(percpu=True)
    average_cpu_x = 0
    for j in range(len(cpu_labels)):
        if sample_size_actual >= sample_size:
            cpu_data[cpu_labels[j]].popleft()
        cpu_data_read = read[j]
        cpu_data[cpu_labels[j]].append(cpu_data_read)
        cpu_ds[j].trigger('data', x, cpu_data[cpu_labels[j]])
        average_cpu_x = average_cpu_x + cpu_data_read

    # average CPU usage
    global average_cpu_sample_size, average_cpu
    average_cpu = average_cpu * average_cpu_sample_size
    average_cpu_sample_size = average_cpu_sample_size + 1
    average_cpu = (average_cpu + (average_cpu_x / 4)) / average_cpu_sample_size

    text = """<h2 style="color :""" + text_color + """;">""" + \
           "&nbsp; &nbsp; Average CPU utilization over last " + str(average_cpu_sample_size) + \
           " sample is " + str(round(average_cpu, 2)) + """</h2>"""
    average_cpu_display.text = text

    volts = []
    for j in range(len(volt_labels) - 1):
        volts.append(open('/sys/class/hwmon/hwmon0/in' + str(j + 1) + '_input', 'r').read())
    volts = [j.replace('\n', '') for j in volts]
    volts.append(int((open('/sys/class/hwmon/hwmon1/in1_input', 'r').read()).replace('\n', '')))

    for j in range(len(volt_labels)):
        if sample_size_actual >= sample_size:
            volt_data[volt_labels[j]].popleft()
        volt_read = int(volts[j])
        volt_data[volt_labels[j]].append(volt_read)
        if (volt_read < min_volt[j]) or (volt_read > max_volt[j]):
            min_volt[j] = min(min_volt[j], int(volts[j]))
            max_volt[j] = max(max_volt[j], int(volts[j]))
            volt_data_table.source.trigger('data', volt_data_table.source, volt_data_table.source)

    temperatures = []
    for j in range(len(temp_labels)):
        temperatures.append(open('/sys/class/hwmon/hwmon0/temp' + str(j + 1) + '_input', 'r').read())
    temperatures = [j.replace('\n', '') for j in temperatures]
    for j in range(len(temp_labels)):
        if sample_size_actual >= sample_size:
            temp_data[temp_labels[j]].popleft()
        temperature_read = (float(temperatures[j])) / 1000
        temp_data[temp_labels[j]].append(temperature_read)
        if (temperature_read < min_temp[j]) or (temperature_read > max_temp[j]):
            min_temp[j] = min(min_temp[j], temperature_read)
            max_temp[j] = max(max_temp[j], temperature_read)
            temp_data_table.source.trigger('data', temp_data_table.source, temp_data_table.source)
    temp_ds[0].trigger('data', x, temp_data[temp_labels[0]])

    ina260_current = (open('/sys/class/hwmon/hwmon1/curr1_input', 'r').read()).replace('\n', '')
    if sample_size_actual >= sample_size:
        current_data.popleft()
    current_data.append(int(ina260_current))
    current_ds.trigger('data', x, current_data)

    ina260_power = int((open('/sys/class/hwmon/hwmon1/power1_input', 'r').read()).replace('\n', '')) / 1000000
    if sample_size_actual >= sample_size:
        power_data.popleft()
    power_data.append(ina260_power)
    power_ds.trigger('data', x, power_data)

    # Mem line chart
    mem_num = get_mem("MemFree")
    if sample_size_actual >= sample_size:
        mem_data["MemFree"].popleft()
    mem_data["MemFree"].append(mem_num)
    mem_ds.trigger('data', x, mem_data["MemFree"])

    # Memory usage Horizontal bar chart
    mem_bar_total[0] = get_mem('MemTotal')
    mem_bar_available[0] = get_mem('MemAvailable')
    mem_bar_used[0] = mem_bar_total[0] - mem_bar_available[0]
    mem_bar_percent[0] = 100 * mem_bar_used[0] / max(mem_bar_total[0], 1)
    mem_bar_total[1] = get_mem('SwapTotal')
    mem_bar_available[1] = get_mem('SwapFree')
    mem_bar_used[1] = mem_bar_total[1] - mem_bar_available[1]
    mem_bar_percent[1] = 100 * mem_bar_used[1] / max(mem_bar_total[1], 1)
    mem_bar_total[2] = get_mem('CmaTotal')
    mem_bar_available[2] = get_mem('CmaFree')
    mem_bar_used[2] = mem_bar_total[2] - mem_bar_available[2]
    mem_bar_percent[2] = 100 * mem_bar_used[2] / max(mem_bar_total[2], 1)
    mem_percent_ds.trigger('data', mem_bar_label, mem_bar_percent)

    if sample_size_actual < sample_size:
        sample_size_actual = sample_size_actual + 1


#margin:  Margin-Top, Margin-Right, Margin-Bottom and Margin-Left
user_interface = column(reset_button, input_sample_size, input_interval, background=bg_color, margin=(50, 50, 50, 100))

curdoc().add_root(column(row(title, align='center'),
                         average_cpu_display,
                         row(cpu_plot, user_interface, background=bg_color),
                         row(mem_plot, mem_plot_hbar, background=bg_color),
                         row(power_plot, current_plot, temp_plot, background=bg_color),
                         row(volt_data_table, temp_data_table, background=bg_color),
                         background=bg_color))

# Add a periodic callback to be run every 1000 milliseconds
callback = curdoc().add_periodic_callback(update, interval * 1000)
