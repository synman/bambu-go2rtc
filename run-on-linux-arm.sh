#!/usr/bin/env bash

CWD=$(pwd)
BASEDIR=$(dirname "$0")
cd $BASEDIR
./go2rtc_linux_arm64 --config go2rtc.yaml
cd $CWD
