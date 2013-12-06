from django.test import TestCase

from . import factories
from ..models import User, UserSettings


class UserTest(TestCase):

    def test_make_objects(self):
        for _ in range(5):
            user = factories.UserFactory()
            self.assertTrue(isinstance(user, User))


class UserSettingsTest(TestCase):

    def test_make_objects(self):
        for _ in range(5):
            user = factories.UserFactory()
            usersettings = factories.UserSettingsFactory()
            self.assertTrue(isinstance(usersettings, UserSettings))