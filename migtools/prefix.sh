#!/bin/sh
# author: zhangpan05
# list no parent pages

OUTF=prefix.log

function errpro() {
	if [ $# -eq 2 ]; then
		echo "$1" >&2
		[ "$2" -ne 0 ] && exit "$2"
	elif [ $# -eq 1 ]; then
		echo "$1" >&2
	fi
}

function prefix() {
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
		# check if parent is in first line and then add meta info in first line
		if sed -ne '1{p;q}' "$file" | grep -q 'META:TOPICPARENT'; then
			sed -f - -i "$file" <<EOF
1{i\
%META:TOPICINFO{author="TWikiGuest" date="$(stat -c %Z $file)" format="1.1" reprev="1.1" version="1.1"}%
q}
EOF
			echo "add meta: $file" >> $OUTF
			prefix "$file"
			return
		fi
		basename "$file"
	elif [ ! -f "${fpath}/${parent}.txt" ]; then
		echo "$file->$parent" >&2
	else
		case "$parent" in
			WebLeftBar|WebChanges|WebSearch|WebTopicList|WebNotify|WebPreferences|WebRss)
				echo "${file}->WebHome" >&2
				;;
			${fname%.*}) # self parent loop
				echo "remove parent line $file" >> $OUTF
				sed -ie '2d' "$file"
				;;
		esac
	fi
}

function main() {
	[ $# -ne 1 ] && errpro "$0 path" 1
	fpath="$1"
	! [ -d "$fpath" ] && errpro "Invalid path: $fpath" 1

	: > $OUTF
	for file in "$fpath"/*.txt; do
		prefix "$file"
	done
}

main $@

# vim: ts=4 sts=4 sw=4
