import sys

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Set the default site name and domain to the ones specified in
        the settings file.'''

    def handle(self, *args, **options):
        site_id_one = Site.objects.get(id=1)

        if site_id_one:
            site_id_one.name = settings.DEFAULT_SITE_NAME
            site_id_one.domain = settings.DEFAULT_SITE_DOMAIN
            site_id_one.save()
        else:
            sys.stdout.write('No sites found.\n')
            sys.exit(1)