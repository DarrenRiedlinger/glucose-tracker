from django.test import TestCase

from . import factories
from ..models import UserSettings


class UserSettingsTest(TestCase):

    def test_make_objects(self):
        for _ in range(5):
            usersettings = factories.UserSettingsFactory()
            self.assertTrue(isinstance(usersettings, UserSettings))