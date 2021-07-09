import subprocess
from functools import partial
from bokeh.models import Button, Paragraph, Div, CustomJS
from bokeh.layouts import layout, row, column, gridplot

import global_var

title = Div(
    text="""<h1 style="color :""" + global_var.text_color + """; text-align :center">Kria Zynq MPSoc Application Cockpit</h1>""",
    width=600)


def xmutil_unloadapp():
    if current_command:
        terminate_app()
    subprocess.run(["sudo", "xmutil", "unloadapp"])
    draw_apps()
    draw_app_run_buttons()
    layout2.children[5] = column(load_buttons)
    layout2.children[1] = active_app_print
    layout2.children[2] = row(run_buttons)


unload_button = Button(label="Unloadapp", width=600, button_type='primary')
unload_button.on_click(xmutil_unloadapp)


# Apps!!!!!###########################################################################################################
def xmutil_loadapp(app_name):
    if current_command:
        print("\nError: unexpected command:", current_command, "\n")
    command = str('sudo xmutil loadapp ' + app_name)
    subprocess.run(command, shell=True, capture_output=True)
    draw_apps()
    draw_app_run_buttons()
    layout2.children[5] = column(load_buttons)
    layout2.children[1] = active_app_print
    layout2.children[2] = row(run_buttons)


# list out applications - currently listpackage doesnt return stdout correctly, temporarily use a fixed string for dev
# listapp_output = subprocess.run(['sudo dfx-mgr-client -listPackage | grep kv260'], shell=True, stdout=subprocess.PIPE)
# print("list app output", listapp_output.stdout)
load_buttons = []
active_app_print = Div(
    text="""<h2 style="color :""" + global_var.text_color + """; text-align :center">Active Accelerator: None</h2>""",
    width=600)
active_app = "None"


def draw_apps():
    global load_buttons
    global active_app_print
    global active_app
    active_app = "None"

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


app_print = Div(
    text="""<h2 style="color :""" + global_var.text_color + """; text-align :left">Available Accelerators on Local  
    System, click blue options to load: </h2>""", width=800)
draw_apps()
current_command = None


def terminate_app():
    global current_command
    current_command.terminate()
    current_command = None


def run_app(run_command):
    global current_command
    if current_command:
        terminate_app()
    print("run_command:", run_command, "\n\n")
    current_command = subprocess.Popen(run_command, shell=True)
    print("\n\ncurrent command: ", current_command, "\n\n")


run_buttons = []


def draw_app_run_buttons():
    global run_buttons
    global active_app
    run_buttons = []
    if active_app == "None":
        return
    less_cmd = 'less som_dashboard/commands/' + active_app + '_cmds.txt'
    print(less_cmd)
    less_return = subprocess.run(less_cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    run_commands_txt = less_return.stdout.decode("utf-8")
    if "No such file" in run_commands_txt:
        return
    run_commands = run_commands_txt.split('\n')
    for commands in run_commands:
        x = commands.split(',')
        button = Button(label=x[0], width=300, button_type='primary')
        button.on_click(partial(run_app, run_command=x[1]))
        run_buttons.append(button)


draw_app_run_buttons()

# packages!!###########################################################################################################

package_print = Div(
    text="""<h2 style="color :""" + global_var.text_color + """; text-align :center">Available Reference Design 
    Package, click to download: </h2>""",
    width=600)


def dnf_install(app_name):
    command = str('sudo dnf install ' + app_name + " -y")
    print("execute command: ", command)
    subprocess.call(command, shell=True)
    print("finished command: ", command)
    draw_pkgs()
    layout2.children[7] = column(pkgs_buttons)
    draw_apps()
    layout2.children[5] = column(load_buttons)


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
    [title],  # 0
    [active_app_print],  # 1
    row(run_buttons),  # 2
    [unload_button],  # 3
    [app_print],  # 4
    column(load_buttons),  # 5
    [package_print],  # 6
    column(pkgs_buttons),  # 7
])
layout2.background = global_var.bg_color
