#!/usr/bin/env sh
#
# Copyright (c) 2015 Z <yunxinyi@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer
#    in this position and unchanged.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# ===============================================================
#
# Filename:	service.sh
#
# Author:		Z
# Email:		yunxinyi@gmail.com
# Created:		[2015-09-07 10:51:34 CST]
# Last-update:	2015-09-07 10:51:34 CST
# Description:  SolrCloud and Zookeeper service
#
# Version:		0.0.1
# Revision:		[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# ===============================================================
#

usage() {
	cat >&2 << EOF
Usage:
	$0 [start|status|stop|status|list|init|post]
Options:
	start	start SolrCloud and Zookeeper
	stop	stop SolrCloud and Zookeeper
	restart	restart SolrCloud and Zookeeper
	status	print the status of SolrCloud and Zookeeper
	deploy	deploy SolrCloud and Zookeeper
	list	list collections of SolrCloud
	init	setup collections, shards and replications for SolrCloud
	post	post sample data to SolrCloud
EOF
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
			tar zxf ~/Downloads/solr-4.10.3.tgz -C .
			tar zxf ~/Downloads/zookeeper-3.4.6.tar.gz -C .
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
			cat >&2 << EOF
$0: Unknown option: '$1'
Use \`$0 --help' for a complete list of options.
EOF
			;;
	esac
}

if [ $# -ne 1 ]; then
	set -- '--help'
fi
main "$@"
