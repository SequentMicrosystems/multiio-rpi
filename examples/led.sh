#!/usr/bin/bash
set -e

function on_exit() {
	multiio 0 ledwr 0
	exit
}
trap on_exit EXIT

LED_NO=6

len=2
if [[ $1 =~ '^[0-9]+$' ]]; then
	len=$1
fi
if ((len >= LED_NO)); then
	len=$LED_NO
fi

echo "Displaying a snake animation with length $len."
echo "Press ctrl-c to interrupt."

multiio 0 ledwr 0

while true; do
	for ((i = 1; i <= $len; i++)); do
		multiio 0 ledwr $i 1
		sleep 0.1
	done
	for ((i = $(($len + 1)); i <= $LED_NO; i++)); do
		multiio 0 ledwr $i 1
		multiio 0 ledwr $((i - len)) 0
		sleep 0.1
	done
	for ((i = $((LED_NO - len + 1)); i <= $LED_NO; i++)); do
		multiio 0 ledwr $i 0
		sleep 0.1
	done
done
