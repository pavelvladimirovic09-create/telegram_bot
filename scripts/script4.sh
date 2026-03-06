#!/bin/bash

for (( i=1; i<=10; i++ )); do
	echo "El: $i"
done

for i in {2..5}; do
	echo "El: $i"
done

i=0
while [ $i -lt 10 ]; do
	echo "El: $i"
	i=$(($i+1))
done
