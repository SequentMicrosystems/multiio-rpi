#!/usr/bin/bash

while true; do
	for ((i = 1; i <= 6; i++)); do
		multiio 0 ledwr $i 1
		sleep 0.1
	done
	for ((i = 1; i <= 6; i++)); do
		multiio 0 ledwr $i 0
		sleep 0.1
	done
done
