#!/bin/bash

read -p "Введите число" num

if [ "$num" == 5 ]; then
	ls
elif [ "$num" > 10 ]; then
	echo "number is bigger than 10"
else
	read -p "Enter your name: " name
	echo "$name"
fi

echo "$num"
