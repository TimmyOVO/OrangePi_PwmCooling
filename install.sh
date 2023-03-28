#!/usr/bash

curl -L -o /disk1/auto_fan_speed.py https://raw.githubusercontent.com/TimmyOVO/OrangePi_PwmCooling/main/cooling.py
curl -L -o /etc/systemd/system/thermal_control.service https://raw.githubusercontent.com/TimmyOVO/OrangePi_PwmCooling/main/thermal_control.service

systemctl start thermal_control.service
systemctl enable thermal_control.service
