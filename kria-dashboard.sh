#!/bin/bash
#*******************************************************************************
#
# Copyright (C) 2019 Xilinx, Inc.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies  of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#**********************************************************************

ip=""

# Preferred devices in order
for dev in eth0 end0 eth1 end1; do
    ip link show "$dev" >/dev/null 2>&1 || continue
    temp_ip="$(ip -4 -o addr show dev "$dev" scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | head -n1)"
    if [ -n "$temp_ip" ]; then
        ip="$temp_ip"
        break
    fi
done

# Fallback: pick first global IPv4 on any interface
if [ -z "$ip" ]; then
    ip="$(ip -4 -o addr show scope global | awk '{print $4}' | cut -d/ -f1 | head -n1)"
fi


python_path=($(python3 -m site | grep packages | grep usr | sed 's/,//g' | sed 's/ //g'| sed 's/^.//;s/.$//'))

for ((i=0;i<${#python_path[@]}; i++)); do
    if [ -d "${python_path[i]}/kria-dashboard" ];
    then
        python_path=${python_path[i]}
        break
    fi
done

if [ -z $ip ]; then
     echo "Cant find IP addr, please call /usr/bin/kria-dashboard.sh after assigning IP addr"
     exit 1
else
    echo "SOM Dashboard will be running at http://$ip:5006/kria-dashboard"
    bokeh serve --show --allow-websocket-origin=$ip:5006 $python_path/kria-dashboard
fi
