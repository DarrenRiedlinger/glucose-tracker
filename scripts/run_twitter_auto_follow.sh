#!/bin/bash

VIRTUALENV_DIR=/webapps/glucosetracker
SCRIPT_DIR=$VIRTUALENV_DIR/glucose-tracker/scripts/

# Activate the virtual environment
source $VIRTUALENV_DIR/bin/activate
source $VIRTUALENV_DIR/bin/postactivate

# Run the script
cd $SCRIPT_DIR
exec python twitter_auto_follow.py