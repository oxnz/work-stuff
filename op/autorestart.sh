#!/bin/bash
#set -x

TOMCAT_NAME="tomcat-dm"
TOMCAT_HOME="/home/work/local/$TOMCAT_NAME"
TOMCAT_ID="[/]home/work/local/$TOMCAT_NAME/bin/bootstrap.jar"
USER=work


main() {
	local opt="$1"
	case "$opt" in
		pid) # show pid
			ps -ef | grep $TOMCAT_ID | awk '{ print $2 }'
			;;
		restart)
			main stop
			main start
			;;
		alive) # test if specified program is alive
			ps -ef | grep $TOMCAT_ID > /dev/null 2>&1
			;;
		stop) # use force to invoke kill with -9
			if  main alive; then
				_pid="$(main pid)"
				if [ -n "$_pid" ]; then
					if [ "$2" = "force" ]; then
						kill -9 "$_pid"
						echo "$(date '+%FT%T'): kill -9 "$pid""
					else
						kill "$_pid"
						echo "$(date '+%FT%T'): kill "$pid""
					fi
					sleep 2
					if main alive; then
						main stop force
					fi
				fi
			fi
			;;
		start)
			for i in 4 6 8 10 12; do
				cd "$TOMCAT_HOME/bin" && ./startup.sh || echo "$TOMCAT_HOME/bin not exists" >&2
				echo "$(date '+%FT%T'): start $pid"
				sleep "$i"
				if main alive; then
					break
				fi
			done
			;;
		help)
			echo "options:"
			egrep '^\s+\w+\)' "$0"
			;;
		*)
			echo "Invalid option: $1" >&2
			;;
	esac
}

main "$@"
