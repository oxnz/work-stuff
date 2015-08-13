#!/bin/sh
# fix missing parent problem

if [ $# -ne 1 ]; then
	echo "Usage: $0 rsbfname" >&2
	exit 1
fi

RSBFNAME="$1"

cmdfmt="sed -i '1 a\\\\\n%s\n' \"%s\""

awk -v cmdfmt="$cmdfmt" -F '->' 'BEGIN {
	printf("%s: start fix missing parent\n", strftime("%F %T %Z"));
}

{
	if ($1 ~ "WebHome.txt" || $1 ~ /^\s*$/) {
		next;
	}
	if ($2 == "WebLeftBar" || $2 == "WebChanges" || $2 == "WebSearch" \
		|| $2 == "WebTopicList" || $2 == "WebNotify" || $2 == "WebPreferences" \
		|| $2 == "WebRss") {
		$2 = "WebHome";
	}
	pline = "%META:TOPICPARENT{name=\""$2"\"}%";
	cmd = sprintf(cmdfmt, pline, $1);
	print cmd;
	ret = system(cmd);
	if (0 != ret)
		printf("%s none zero exit status(%d) of command(%s)\n", strftime("%F %T %Z"), ret, cmd) | "cat 1>&2"
}

END {
	printf("%s: fix missing parent done\n", strftime("%F %T %Z"));
}' "$RSBFNAME" 2>&1 | tee postfix.log
