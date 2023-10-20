#!/usr/bin/bash
set -e

multiio 0 relwr 0

while true; do
	# Start relays
	multiio 0 relwr 1 1
	sleep 0.1
	multiio 0 relwr 2 1
	sleep 0.9
	# Stop relays
	multiio 0 relwr 1 0
	sleep 0.1
	multiio 0 relwr 2 0
	sleep 0.9
done
