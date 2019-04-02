#!/bin/sh
# 
# ===============================================================
#
# Filename:	mysql_monitor.sh
#
# Author:		Oxnz
# Email:		yunxinyi@gmail.com
# Created:		2016-09-02 11:19:58 CST
# Last-update:	2016-09-02 11:19:58 CST
# Description: ANCHOR
#
# Version:		0.0.1
# Revision:	[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# License:
# Copyright (c) 2016 Oxnz
#
# Distributed under terms of the [LICENSE] license.
# [license]
#
# ===============================================================
#


OUTDIR='./watchlog'
MAXSZ=10000000000

watch() {
	/home/work/local/mysql/bin/mysql -uusername -ppassword -Pport -hhost << EOF | grep -v 'Id' | grep -v 'show processlist'
	show processlist;
	EOF
}

main() {
	local logf="$OUTDIR/watch.log"
	echo "$(date '+%FT%T'): start watch" >> "$logf"
	while true; do
		for i in {1..3}; do
			watch > "$OUTDIR/$(date '+%s')"
			sleep 1
		done
		sz="$(du -sb $OUTDIR | cut -f 1)"
		if [ "$sz" -gt "$MAXSZ" ]; then
			echo "$(date '+%FT%T'): output dir occupies more thant $MAXSZ" >> "$logf"
			break
		fi
	done
}

main "$@"
