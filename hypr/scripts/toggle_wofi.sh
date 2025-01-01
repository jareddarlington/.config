#!/bin/bash

# Check if Wofi is running, and toggle
if pgrep -x "wofi" > /dev/null
then
    pkill wofi
else
    wofi --show drun &
fi
