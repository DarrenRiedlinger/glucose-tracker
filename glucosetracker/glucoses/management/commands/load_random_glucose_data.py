from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth.models import User

from ...tests.factories import GlucoseFactory
from ...models import Glucose


class Command(BaseCommand):
    args = '<username...>'
    help = 'Populate glucose table with random dummy data.'

    def handle(self, *args, **options):
        assert len(args) == 1, 'You must specify a username.'

        try:
            user = User.objects.get(username=args[0])
        except ObjectDoesNotExist:
            user = User.objects.create(username=args[0])
            user.set_password('demo')
            user.save()

        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        for i in GlucoseFactory.get_date_list(start_date, end_date):
            for _ in xrange(4):
                GlucoseFactory(user=user, record_date=i)
