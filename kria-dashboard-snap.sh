#!/bin/bash

$SNAP/bin/bokeh serve --address 0.0.0.0 --allow-websocket-origin=* --show $SNAP/var/opt/kria-dashboard
