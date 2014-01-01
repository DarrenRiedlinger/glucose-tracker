#!/bin/bash

BACKUP_SCRIPT_DIR=/webapps/glucosetracker/glucose-tracker/scripts/

# Activate the virtual environment
cd $BACKUP_SCRIPT_DIR
source ../../bin/activate

# Run the backup script
exec python db_backup.py -t $1