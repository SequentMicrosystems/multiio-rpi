#!/usr/bin/bash

if multiio 0 optedgewr 1 1 && multiio 0 optcntrst 1; then
	echo -n ""
	#echo "Setup completed"
else
	echo "Error on setting up opto channel 1!"
	exit -1
fi

prev=0
echo "Opto couter:"
echo -n 0
while true; do
	cur=$(multiio 0 optcntrd 1)
	if [[ $cur != $prev ]]; then
		echo -en "\e[2K\r$cur"
	fi
	prev=$cur
	sleep 0.05
done
