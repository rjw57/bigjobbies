# This script should not directly be executed. It defines functions common to
# both root_run.sh and user_run.sh.

# Wrap a command such that standard output lines are prefixed by "O:" and
# standard error by "E:".
#
# Inspired by:
# http://serverfault.com/questions/59262
# http://stackoverflow.com/questions/9112979
logcmd()(
    set -o pipefail;
    echo "C:$1";
    shift
    { "$@" 2>&3 | sed 's,^,O:,' >&2; } 3>&1 1>&2 | sed 's,^,E:,'
)

wrap()(
    logcmd "$*" "$@"
)

info()( echo "I:$*" )

error()( echo "E:$*" )

section()( echo "S:$*" )
