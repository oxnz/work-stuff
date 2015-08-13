#!/bin/sh
# author: zhangpan05
# remove parent line

if [ $# -ne 1 ]; then
	echo "Usage: $0 errfile" >&2
	exit 1
fi

errfile="$1"

sed -e 's/\(.*\)->.*$/\1/' "$errfile" | while read file; do
	sed -ie '2d' "$file";
done
