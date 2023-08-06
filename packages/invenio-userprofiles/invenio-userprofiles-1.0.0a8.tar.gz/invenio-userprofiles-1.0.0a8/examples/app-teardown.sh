#!/bin/sh

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# clean environment
[ -e "$DIR/instance" ] && rm $DIR/instance -Rf
[ -e "$DIR/static" ] && rm $DIR/static/ -Rf
[ -e "$DIR/cookiefile" ] && rm $DIR/cookiefile -Rf
