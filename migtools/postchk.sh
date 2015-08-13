#!/bin/sh
# check if fixed are OK.

function postchk() {
	local file="$1"
	local parent=$(sed -ne '2{
b begin
:notfound
s/^.*$//
:found
p
q
:begin
s/%META:TOPICPARENT{name="\(.*\)"}%/\1/
t found
b notfound
}' "$file")
	local fname=$(basename "$file")
	local fpath=$(dirname "$file")

	if [ -z "$parent" ]; then
		echo "$file has no parent"
	elif [ ! -f "${fpath}/${parent}.txt" ]; then
		echo "parent $parent not exist"
	fi
}

function main() {
	if [ $# -ne 1 ]; then
		echo "Usage: $0 errfile" >&2
		exit 1
	fi

	errfile="$1"

	sed -e 's/\(.*\)->.*$/\1/' "$errfile" | while read file; do
		postchk "$file"
	done
}

main $@
