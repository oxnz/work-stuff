#!/usr/bin/env sh
# 
# ===============================================================
#
# Filename:	start.sh
#
# Author:		Oxnz
# Email:		yunxinyi@gmail.com
# Created:		[2015-09-07 10:51:34 CST]
# Last-update:	2015-09-07 10:51:34 CST
# Description: ANCHOR
#
# Version:		0.0.1
# Revision:	[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# License:
# Copyright (c) 2013 Oxnz
#
# Distributed under terms of the [LICENSE] license.
# [license]
#
# ===============================================================
#

usage() {
	echo "Usage: $0 [start|status|stop]" >&2
	exit 1
}

main() {
	case "$1" in
		start)
			for i in 1 2 3; do
				./zookeeper/bin/zkServer.sh start "zoo${i}.cfg"
				if [ $? -ne 0 ]; then
					echo "error start zookeeper 'zoo${i}.cfg'" >&2
					exit 1
				fi
			done
			zkHost="localhost:2181,localhost:2182,localhost:2183"
			for i in 3 2 1; do
				./solr/bin/solr start -cloud -p $((8980+i)) -z "$zkHost"
			done
			;;
		stop)
			./solr/bin/solr stop -all
			for i in 1 2 3; do
				./zookeeper/bin/zkServer.sh stop "zoo${i}.cfg"
			done
			;;
		status)
			./solr/bin/solr status
			for i in 1 2 3; do
				./zookeeper/bin/zkServer.sh status "zoo${i}.cfg"
			done
			;;
		deploy)
#			if [ -d "./solr-4.10.3" ]; then
#				rm -rf "./solr-4.10.3"
#			fi
#			if [ -d "./zookeeper-3.4.6" ]; then
#				rm -rf "./zookeeper-3.4.6"
#			fi
			#tar zxf ~/Downloads/solr-4.10.3.tgz -C .
			#tar zxf ~/Downloads/zookeeper-3.4.6.tar.gz -C .
			for i in 1 2 3; do
				cp zookeeper/conf/zoo_sample.cfg "zookeeper/conf/zoo${i}.cfg"
				sed -i "s/2181/218$i/" "zookeeper/conf/zoo${i}.cfg"
				echo "server.1=localhost:2888:3888" >> "zookeeper/conf/zoo${i}.cfg"
				echo "server.2=localhost:2889:3889" >> "zookeeper/conf/zoo${i}.cfg"
				echo "server.3=localhost:2890:3890" >> "zookeeper/conf/zoo${i}.cfg"
				mkdir -p "zookeeper/data/${i}"
				echo "${i}" > "zookeeper/data/${i}/myid"
				sed -i "s@/tmp/zookeeper@$(pwd)/zookeeper/data/${i}@" "zookeeper/conf/zoo${i}.cfg"
			done
			;;
		restart)
			sh "$0" stop
			sh "$0" start
			;;
		list)
			curl 'http://localhost:8983/solr/admin/collections?action=LIST'
			;;
		init)
			./solr/bin/solr create_collection -c msg -shards 2 -replicationFactor 3
			;;
		post)
			./solr/bin/post -c msg solr/example/exampledocs/*.xml
			;;
		--help)
			usage
			;;
		*)
			echo "Unknown option: '$1'" >&2
			;;
	esac
}

if [ $# -ne 1 ]; then
	set -- '--help'
fi
main "$@"
