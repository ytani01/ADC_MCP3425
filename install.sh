#!/bin/sh
#
# Copyright (c) 2021 Yoichi Tanibayashi
#
MYNAME=`basename $0`
cd `dirname $0`
MYDIR=`pwd`
echo "MYDIR=$MYDIR"

BINDIR="$HOME/bin"
LOGDIR="$HOME/tmp"
BUILD_DIR="$MYDIR/build"

WRAPPER_SRC="wrapper.src"
SH_FILES="adc_mcp3425"

BIN_FILES="v_mon.sh $BUILD_DIR/*"

wrapper2sh() {
    _DST_SH=$BUILD_DIR/$1.sh

    echo "generate: $_DST_SH"
    sed -e "s?%%% CMDNAME %%%?$1?" \
        -e "s?%%% VENVDIR %%%?$VIRTUAL_ENV?" \
        $WRAPPER_SRC > $_DST_SH
    chmod +x $_DST_SH
}

### mkdirs
for d in $BINDIR $LOGDIR $BUILD_DIR; do
    if [ ! -d $d ]; then
        mkdir -pv $d
    fi   
done

### activate venv
if [ -z $VIRTUAL_ENV ]; then
    while [ ! -f ./bin/activate ]; do
        cd ..
        if [ `pwd` = "/" ]; then
            echo
            echo "ERROR] Please create and activate Python3 venv"
            echo
            exit 1
        fi
    done
    . ./bin/activate
fi
echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $MYDIR
echo "[`pwd`]"

### make sh files
for s in $SH_FILES; do
    wrapper2sh $s
done

### install
for f in $BIN_FILES; do
    cp -fv $f $BINDIR
done
