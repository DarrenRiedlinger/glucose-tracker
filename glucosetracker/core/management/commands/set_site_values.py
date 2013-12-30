import sys

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set the default site name and domain to the ones specified in ' \
           'the settings file.'

    def handle(self, *args, **options):
        site_id = settings.SITE_ID

        try:
            site_obj = Site.objects.get(id=site_id)
            site_obj.name = settings.SITE_NAME
            site_obj.domain = settings.SITE_DOMAIN
            site_obj.save()
        except ObjectDoesNotExist:
            sys.stdout.write('Site ID %s not found.\n' % site_id)
            sys.exit(1)