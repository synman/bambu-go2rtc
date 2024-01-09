#!/usr/bin/env bash

CWD=$(pwd)
BASEDIR=$(dirname "$0")
cd $BASEDIR
./go2rtc-mac --config go2rtc.yaml
cd $CWD
