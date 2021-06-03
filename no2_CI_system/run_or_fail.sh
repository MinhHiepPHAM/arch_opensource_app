#!/bin/bash

# helper method for providing error messages for a command
# for example, the comment run_or_fail 'explanation comment' ls -a:
# if "ls -a" fails, the explanation will be printed
run_or_fail() {
	local explanation=$1
	shift
	"$@"
	if [ $? != 0 ]; then
		echo $explanation 1>&2
		exit
	fi
}
