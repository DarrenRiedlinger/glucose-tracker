"""
A simple script to backup the PostgreSQL database.

TODO: Add email alert if exit code is not 0.
"""
import sys
import subprocess
from optparse import OptionParser
from datetime import datetime


DB_USER = 'glucosetracker'
DB_NAME = 'glucosetracker'

ROOT_PATH = r'/webapps/glucosetracker/db_backups'
HOURLY_PATH = r'%s/hourly' % ROOT_PATH
DAILY_PATH = r'%s/daily' % ROOT_PATH

FILENAME_PREFIX = 'glucosetracker.backup'


def main():
    parser = OptionParser()
    parser.add_option('-t', '--type', dest='backup_type',
                      help="Specify either 'hourly' or 'daily'.")

    now = datetime.now()
    hour = str(now.hour).zfill(2)
    day_of_year = str(now.timetuple().tm_yday).zfill(3)

    destination = None
    (options, args) = parser.parse_args()
    if options.backup_type == 'hourly':
        destination = r'%s/%s.h%s' % (HOURLY_PATH, FILENAME_PREFIX, hour)
    elif options.backup_type == 'daily':
        destination = r'%s/%s.d%s' % (DAILY_PATH, FILENAME_PREFIX, day_of_year)
    else:
        parser.error('Invalid argument.')
        sys.exit(1)

    print 'Backing up %s database to %s' % (DB_NAME, destination)
    ps = subprocess.Popen(
        ['pg_dump', '-U', DB_USER, '-Fc', DB_NAME, '-f', destination],
        stdout=subprocess.PIPE
    )

    output = ps.communicate()[0]
    for line in output.splitlines():
        print line


if __name__ == '__main__':
    main()