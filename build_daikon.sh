#!/usr/bin/env bash

set -e

DAIKON_TARBALL=$1
DAIKON_PARENT_DIR=`dirname $1`

echo build_daikon.sh: DAIKON_TARBALL=$DAIKON_TARBALL
echo build_daikon.sh: DAIKON_PARENT_DIR=$DAIKON_PARENT_DIR
echo build_daikon.sh: JAVA_HOME=${JAVA_HOME}

pushd $DAIKON_PARENT_DIR
    DAIKON_SRC_DIR=`tar -tzf ${DAIKON_TARBALL} | head -1 | cut -f1 -d"/"`
    echo build_daikon.sh: DAIKON_SRC_DIR=${DAIKON_SRC_DIR}
    tar xzf $DAIKON_TARBALL
    mv $DAIKON_SRC_DIR daikon-src
    pushd daikon-src
        export DAIKONDIR=`pwd`
        source scripts/daikon.bashrc
        make -C java dcomp_rt.jar
    popd
popd
