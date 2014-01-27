from django.test import TestCase

from .. import utils


class CoreUtilsTest(TestCase):

    known_glucose_conversion_values = (
        {'mg': 40, 'mmol': 2.2 },
        {'mg': 36, 'mmol': 2.0 },
        {'mg': 65, 'mmol': 3.6 },
        {'mg': 70, 'mmol': 3.9 },
        {'mg': 85, 'mmol': 4.7 },
        {'mg': 90, 'mmol': 5.0 },
        {'mg': 110, 'mmol': 6.1 },
        {'mg': 135, 'mmol': 7.5 },
        {'mg': 180, 'mmol': 10.0 },
        {'mg': 169, 'mmol': 9.4 },
        {'mg': 200, 'mmol': 11.1 },
        {'mg': 400, 'mmol': 22.2 },
    )

    def test_to_mmol(self):
        for i in self.known_glucose_conversion_values:
            result = utils.to_mmol(i['mg'])
            self.assertEqual(i['mmol'], result)

    def test_to_mg(self):
        for i in self.known_glucose_conversion_values:
            result = utils.to_mg(i['mmol'])
            self.assertEqual(i['mg'], result)

    def test_round_value(self):
        known_values = (
            (129.55, 129.6),
            (285.42, 285.4),
            (4.76623, 4.8),
            (8.3221, 8.3),
        )

        for value, rounded_value in known_values:
            result = utils.round_value(value)
            self.assertEqual(rounded_value, result)

    def test_glucose_conversion_sanity(self):
        for i in xrange(300):
            mmol = utils.round_value(i*0.1)
            mg = utils.to_mg(mmol)
            result = utils.to_mmol(mg)
            self.assertEqual(mmol, result)

    def test_percent(self):
        known_values = (
            {'part': 3, 'whole': 4, 'percent': 75},

            # Result is undefined, but we'll return 0.
            {'part': 1, 'whole': 0, 'percent': 0},

            {'part': 0, 'whole': 5, 'percent': 0},
            {'part': 1.5, 'whole': 2.5, 'percent': 60},
            {'part': 1.72, 'whole': 5.84, 'percent': 29.5},
        )

        for i in known_values:
            result = utils.percent(i['part'], i['whole'])
            self.assertEqual(i['percent'], result)