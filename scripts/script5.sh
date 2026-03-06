#!/bin/bash

divide() {
	echo "Params: $1 $2"
	if [ "$2 == 0 ]; then
		echo "Error"
	else
		res=$(($1/$2))
		echo "$res"
	fi
}

divide 10 2
divide 10 0
