#!/bin/sh 

if(($#<1))
then
	echo "usage: $0 dir"
	exit 0
fi

ls -1 $1|while read line
do
	sed 's/,/\n/g;s/\./\n/g;s/?/\n/g;s/!/\n/g' $1/$line|sed '/^[[:space:]]*$/d' > $1/$line.sed 
done
