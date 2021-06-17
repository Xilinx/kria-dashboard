# som_dashboard
This repository contains source code for a SOM dashboard. It is implemented using bokeh.
To install Bokeh on 2020.2: 
  sudo pip3 install bokeh==2.1
Information TBD for 2021.1.

to execute, copy all the files onto a directory on SOM platform in a folder (lets say we name it som_dashboard), and then execute from that directory:
  sudo bokeh serve --show --allow-websocket-origin=*IP_ADDRESS*:5006 som_dashboard/
in a browser go to the following url:
  http://*IP_ADDRESS*:5006/som_dashboard


Current view:
![Alt text](screenshot.PNG?raw=true "Title")
