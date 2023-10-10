#!/usr/bin/bash

while true; do
	multiio 0 servowr 1 120
	sleep 1
	multiio 0 servowr 1 -120
	sleep 1
done
