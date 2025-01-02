#!/usr/bin/env python

import json

# available os icons
os_icons = {"default": "", "arch": "󰣇"}

# reads os/distro
try:
    with open("/etc/os-release", "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("ID="):
            os = line.split("=")[1].strip().strip('"')
            break
except Exception as e:
    os = ""

# sets icon based on os
icon = os_icons[os] if os in os_icons else os_icons["default"]

# formats json output
out_data = {
    "text": f"{icon}",
    "alt": os,
}

# prints json output
print(json.dumps(out_data))
