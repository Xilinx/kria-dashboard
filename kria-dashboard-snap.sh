#!/bin/bash

echo "SOM Dashboard will be running at http://$(hostname -I | cut -d' ' -f1):5006/kria-dashboard"
$SNAP/bin/bokeh serve --address 0.0.0.0 --allow-websocket-origin=* --show $SNAP/var/opt/kria-dashboard
