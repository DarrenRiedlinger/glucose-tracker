#!/bin/bash

VIRTUALENV_DIR=/webapps/glucosetracker
BACKUP_SCRIPT_DIR=$VIRTUALENV_DIR/glucose-tracker/scripts/

# Activate the virtual environment
source $VIRTUALENV_DIR/bin/activate
source $VIRTUALENV_DIR/bin/postactivate

# Run the backup script
cd $BACKUP_SCRIPT_DIR
exec python db_backup.py -t $1