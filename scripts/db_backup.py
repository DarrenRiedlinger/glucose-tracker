"""
A simple script to backup the PostgreSQL database.

TODO: Add email alert if exit code is not 0 or exceptions occur.
"""
import os
import sys
import subprocess
from optparse import OptionParser
from datetime import datetime

import boto
from boto.s3.key import Key

DB_USER = 'glucosetracker'
DB_NAME = 'glucosetracker'

BACKUP_PATH = r'/webapps/glucosetracker/db_backups'

FILENAME_PREFIX = 'glucosetracker.backup'

# Amazon S3 settings.
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_BUCKET_NAME = 'glucosetracker-db-backups'


def main():
    parser = OptionParser()
    parser.add_option('-t', '--type', dest='backup_type',
                      help="Specify either 'hourly' or 'daily'.")

    now = datetime.now()

    filename = None
    (options, args) = parser.parse_args()
    if options.backup_type == 'hourly':
        hour = str(now.hour).zfill(2)
        filename = '%s.h%s' % (FILENAME_PREFIX, hour)
    elif options.backup_type == 'daily':
        day_of_year = str(now.timetuple().tm_yday).zfill(3)
        filename = '%s.d%s' % (FILENAME_PREFIX, day_of_year)
    else:
        parser.error('Invalid argument.')
        sys.exit(1)

    destination = r'%s/%s' % (BACKUP_PATH, filename)

    print 'Backing up %s database to %s' % (DB_NAME, destination)
    ps = subprocess.Popen(
        ['pg_dump', '-U', DB_USER, '-Fc', DB_NAME, '-f', destination],
        stdout=subprocess.PIPE
    )
    output = ps.communicate()[0]
    for line in output.splitlines():
        print line

    print 'Uploading %s to Amazon S3...' % filename
    upload_to_s3(destination, filename)


def upload_to_s3(source_path, destination_filename):
    """
    Upload a file to an AWS S3 bucket.
    """
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_BUCKET_NAME)
    k = Key(bucket)
    k.key = destination_filename
    k.set_contents_from_filename(source_path)


if __name__ == '__main__':
    main()