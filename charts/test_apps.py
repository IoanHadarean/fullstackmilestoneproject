from django.apps import apps
from django.test import TestCase
from charts.apps import ChartsConfig


class ChartsAppConfigTest(TestCase):
    """Class for testing charts app config"""

    def test_charts_app_config(self):
        self.assertEqual(ChartsConfig.name, 'charts')
        self.assertEqual(apps.get_app_config('charts').name, 'charts')
