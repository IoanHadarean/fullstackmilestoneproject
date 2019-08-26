from django.apps import apps
from django.test import TestCase
from charts.apps import ChartsConfig

class ChartsConfigTest(TestCase):
    
    def test_charts_config(self):
        self.assertEqual(ChartsConfig.name, 'charts')
        self.assertEqual(apps.get_app_config('charts').name, 'charts')
        