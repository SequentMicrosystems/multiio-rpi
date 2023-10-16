#!/usr/bin/bash

multiio 0 dodwr 0

while true; do
	multiio 0 dodwr 1 1
	sleep 0.1
	multiio 0 dodwr 2 1
	sleep 0.9
	multiio 0 dodwr 2 0
	sleep 0.1
	multiio 0 dodwr 1 0
	sleep 0.9
done
