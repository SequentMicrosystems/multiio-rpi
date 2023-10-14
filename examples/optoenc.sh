#!/usr/bin/bash

multiio 0 optencwr 1 1

prev=0
echo "Opto couter:"
echo -n 0
while true; do
	cur=$(multiio 0 optcntencrd 1)
	if [[ $cur != $prev ]]; then
		echo -en "\e[2K\r$cur"
	fi
	prev=$cur
	sleep 0.05
done
