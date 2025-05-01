
<h1 align="center">KRIA SOM DASHBOARD</h1>

## Introduction
This repository contains the source code of Kria SOM dashboard tool which provides the debugging information of Kria SOM.

## How to use

Kria Yocto/PetaLinux has Bokeh and dashboard installed, and does not require installation. The Bokeh server is also started automatically, URL is printed out before login.

Kria Ubuntu 24.04 OS also have Kria-dashboard baked in. The url currently does not print out, but you can check for the startup command using this:

```sudo ps -p $(sudo lsof -t -iTCP:5006 -sTCP:LISTEN) -o args=``` 

And this will be the URL:    ```http://*IP_ADDRESS*:5006/kria-dashboard```

Kria Ubuntu 22.04 does not have Kria-dashboard baked in, but it is in the Xilinx PPA and can be installed after Linux boot and setup ([KD240]([https://xilinx.github.io/kria-apps-docs/kd240/build/html/docs/kria_starterkit_linux_boot.html](https://xilinx.github.io/kria-apps-docs/kd240/build/html/docs/linux_boot.html)), [KR260](https://xilinx.github.io/kria-apps-docs/kr260/build/html/docs/linux_boot.html), [KV260](https://xilinx.github.io/kria-apps-docs/kv260/2022.1/build/html/docs/linux_boot.html))

```bash
sudo apt search kria-dashboard
sudo apt install kria-dashboard
```

To start Bokeh server manually, use one of the following commands:

```bash
sudo bokeh serve --show --allow-websocket-origin=*IP_ADDRESS*:5006 /usr/lib/python3.9/site-packages/kria-dashboard 
#tio: use 
#   sudo find / -iname "kria-dashboard"
# to find the folder if its not in the above python path
```

You can also manually clone kria-dashboard to use:

```bash
git clone https://github.com/Xilinx/kria-dashboard.git
sudo bokeh serve --show --allow-websocket-origin=*IP_ADDRESS*:5006 kria-dashboard
```

In a browser go to the following url:

    http://*IP_ADDRESS*:5006/kria-dashboard

Current view:
![Alt text](snapshot1.PNG?raw=true "Title")

## License

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License.

You may obtain a copy of the License at apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the Licens
