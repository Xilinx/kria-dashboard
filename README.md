# SOM Dashboard
This repository contains source code for a SOM dashboard. It is implemented using bokeh.

To install Bokeh on 2020.2: 

    
    sudo pip3 install bokeh==2.1
    
    
To install Bokeh on 2021.1:

    
    sudo pip3 install panel
    
    
2021.2 has Bokeh and dashboard installed, and does not require installation. 

to execute, copy all the files onto a directory on SOM platform in a folder (lets say we name it som_dashboard), and then execute outside that directory:

  	
    sudo bokeh serve --show --allow-websocket-origin=*IP_ADDRESS*:5006 som_dashboard/
    

in a browser go to the following url:

    
    http://*IP_ADDRESS*:5006/som_dashboard
    

Current view:
![Alt text](snapshot1.PNG?raw=true "Title")
![Alt text](snapshot2.PNG?raw=true "Title")

# License
Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License.

You may obtain a copy of the License at apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the Licens
