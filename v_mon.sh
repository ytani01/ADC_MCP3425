#!/bin/sh
#
# Copyright (c) 2021 Yoichi Tanibayashi
#
MYNAME=`basename $0`
MYDIR=`dirname $0`

LOGDIR=$HOME/tmp
LOGFILE=$LOGDIR/v.log

CMDLINE="adc_mcp3425.sh watch"

if [ -f $LOGFILE ]; then
   mv -fv $LOGFILE $LOGFILE.1
fi

$CMDLINE | tee $LOGFILE
