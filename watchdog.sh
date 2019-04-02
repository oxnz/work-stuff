#!/bin/sh
# 
# ===============================================================
#
# Filename:	watchdog.sh
#
# Author:		Oxnz
# Email:		yunxinyi@gmail.com
# Created:		2016-09-02 11:09:44 CST
# Last-update:	2016-09-02 11:09:44 CST
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

while true; do
	sleep 30
	if ! ps -ef | grep '[t]omcat-alfresco' > /dev/null 2>&1; then
		cd /home/work/local/tomcat-alfresco/bin && ./startup.sh
		echo "$(date) start"
	fi
done
