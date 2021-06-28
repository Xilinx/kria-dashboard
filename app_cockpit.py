import subprocess
from functools import partial
from bokeh.models import Button, Paragraph, Div, CustomJS
from bokeh.layouts import layout, row, column, gridplot

import global_var

title = Div(
    text="""<h1 style="color :""" + global_var.text_color + """; text-align :center">Kria Zynq MPSoc Application Cockpit</h1>""",
    width=600)


def xmutil_unloadapp():
    subprocess.run(['sudo xmutil unloadapp'], shell=True, capture_output=True)
    draw_apps()
    layout2.children[3] = column(load_buttons)
    layout2.children[1] = active_app_print


unload_button = Button(label="Unloadapp", width=600, button_type='primary')
unload_button.on_click(xmutil_unloadapp)


# Apps!!!!!###########################################################################################################
def xmutil_loadapp(app_name):
    command = str('sudo xmutil loadapp ' + app_name)
    subprocess.run(command, shell=True, capture_output=True)
    draw_apps()
    layout2.children[3] = column(load_buttons)
    layout2.children[1] = active_app_print


# list out applications - currently listpackage doesnt return stdout correctly, temporarily use a fixed string for dev
# listapp_output = subprocess.run(['sudo dfx-mgr-client -listPackage | grep kv260'], shell=True, stdout=subprocess.PIPE)
# print("list app output", listapp_output.stdout)
load_buttons = []
active_app_print = Div(
    text="""<h2 style="color :""" + global_var.text_color + """; text-align :center">Active Accelerator: None</h2>""",
    width=600)


def draw_apps():
    global load_buttons
    global active_app_print
    active_app = "None"
    # listapp_output = """                                       Accelerator           Type    Active
    #                                     kv260-smartcam       XRT_FLAT         1
    #                                           kv260-dp       XRT_FLAT         0
    #                                               base       XRT_FLAT         0"""
    listapp_output = subprocess.run(['sudo dfx-mgr-client -listPackage'], shell=True,
                                    stdout=subprocess.PIPE).stdout.decode("utf-8")

    print("\n", listapp_output, "\n")
    listapp = listapp_output.split("\n")
    apps = []
    load_buttons = []
    for i in range(len(listapp) - 1):
        x = listapp[i].split()
        print("\n x is ", x, " i is ", i, "\n")
        if x and x[0] != "Accelerator":
            apps.append(x[0])
            if x[4] != "-1":
                active_app = x[0]

    active_app_print = Div(
        text="""<h2 style="color :""" + global_var.text_color + """; text-align :center">Active Accelerator: """ + active_app + """</h2>""",
        width=600)

    for i in range(len(apps)):
        load_buttons.append(Button(label=apps[i], width=300, button_type='primary'))
        if active_app != "None":
            if apps[i] == active_app:
                load_buttons[i].button_type = 'success'
                load_buttons[i].js_on_click(
                    CustomJS(code='alert("This Accelerator is already loaded, Unloadapp first!");'))
            else:
                load_buttons[i].button_type = 'default'
                load_buttons[i].js_on_click(CustomJS(code='alert("Unloadapp First!");'))
        else:
            load_buttons[i].on_click(partial(xmutil_loadapp, app_name=apps[i]))


draw_apps()
# packages!!###########################################################################################################

package_print = Div(
    text="""<h2 style="color :""" + global_var.text_color + """; text-align :center">Packages to Download</h2>""",
    width=600)


def dnf_install(app_name):
    command = str('sudo dnf install ' + app_name + " -y")
    print("execute command: ", command)
    subprocess.call(command, shell=True)
    print("finished command: ", command)
    draw_pkgs()
    layout2.children[5] = column(pkgs_buttons)


pkgs_buttons = []


def draw_pkgs():
    global pkgs_buttons
    # subprocess.run(['sudo dnf update'], shell=True)
    # subprocess.run(['sudo dnf clean all'], shell=True)
    getpkgs_output = subprocess.run(['sudo xmutil getpkgs | grep packagegroup-kv260'], shell=True,
                                    stdout=subprocess.PIPE).stdout.decode("utf-8")
    print("getpkgs_output", getpkgs_output)
    list_pkgs = getpkgs_output.split("\n")
    pkgs_buttons = []
    for i in range(len(list_pkgs) - 1):
        x = list_pkgs[i].split()
        pkgs_buttons.append(Button(label=x[0], width=300, button_type='primary'))
        pkgs_buttons[i].on_click(partial(dnf_install, app_name=x[0]))


draw_pkgs()

layout2 = layout([
    [title],
    [active_app_print],
    [unload_button],
    column(load_buttons),
    [package_print],
    column(pkgs_buttons),
])
layout2.background = global_var.bg_color


def smartcam_mipi_rtsp():
    subprocess.run(['sudo 01.mipi-rtsp.sh'], shell=True)


run_button_smartcam01 = Button(label="MIPI-RTSP", width=200, button_type='primary')
run_button_smartcam01.on_click(smartcam_mipi_rtsp)


def smartcam_mipi_dp():
    subprocess.run(['sudo 02.mipi-dp.sh'], shell=True)


run_button_smartcam02 = Button(label="MIPI-DP", width=200, button_type='primary')
run_button_smartcam02.on_click(smartcam_mipi_dp)
