#!/usr/bin/bash
set -e

ch=1
multiio 0 uoutcal $ch reset
sleep 1
multiio 0 uoutwr $ch 0
sleep 1
multiio 0 uoutcal $ch 0
multiio 0 uoutwr $ch 8
sleep 1
read -p "Measured value: " value
multiio 0 uoutcal $ch $value
