import subprocess
from bokeh.models import Button, Paragraph, Div
from bokeh.layouts import layout, row, column, gridplot

import global_var


title = Div(
    text="""<h1 style="color :""" + global_var.text_color + """; text-align :center">Kria Zynq MPSoc Application Cockpit</h1>""",
    width=450)


def xmutil_unloadapp():
    subprocess.run(['sudo xmutil unloadapp'], shell=True,  capture_output=True)
unload_button = Button(label="Unloadapp", width=200, button_type='primary')
unload_button.on_click(xmutil_unloadapp)


def xmutil_loadapp(app_name):
    command = str ('sudo xmutil loadapp ' + app_name)
    print("executing: ", command)
    subprocess.run(command, shell=True,  capture_output=True)

def load_smartcam():
    xmutil_loadapp('kv260-smartcam')
load_button_smartcam = Button(label="Load SmartCam", width=200, button_type='primary')
load_button_smartcam.on_click(load_smartcam)
def smartcam_mipi_rtsp():
    subprocess.run(['sudo 01.mipi-rtsp.sh'], shell=True)
run_button_smartcam01 = Button(label="MIPI-RTSP", width=200, button_type='primary')
run_button_smartcam01.on_click(smartcam_mipi_rtsp)
def smartcam_mipi_dp():
    subprocess.run(['sudo 02.mipi-dp.sh'], shell=True)
run_button_smartcam02 = Button(label="MIPI-DP", width=200, button_type='primary')
run_button_smartcam02.on_click(smartcam_mipi_dp)

def load_aibox():
    xmutil_loadapp('kv260-aibox-reid')
load_button_aibox = Button(label="Load AIBox", width=200, button_type='primary')
load_button_aibox.on_click(load_aibox)


layout2 = layout(column(row(title, align='center'),
                        unload_button,
                        row(load_button_smartcam, run_button_smartcam01, run_button_smartcam02, background=global_var.bg_color),
                        load_button_aibox,
                        background=global_var.bg_color,))