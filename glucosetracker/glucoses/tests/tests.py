from django.test import TestCase

from . import factories
from ..models import Glucose

class GlucoseTest(TestCase):

    def test_make_objects(self):
        glucose = factories.GlucoseFactory.create()
        self.assertTrue(isinstance(glucose, Glucose))