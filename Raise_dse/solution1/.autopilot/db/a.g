#!/bin/sh
lli=${LLVMINTERP-lli}
exec $lli \
    /home/npschuster/raise_dse/raise_dse/Raise_dse/solution1/.autopilot/db/a.g.bc ${1+"$@"}
