from django.apps import apps
from django.test import TestCase
from search.apps import SearchConfig


class SearchAppConfigTest(TestCase):
    """Class for testing search app config"""

    def test_search_app_config(self):
        self.assertEqual(SearchConfig.name, 'search')
        self.assertEqual(apps.get_app_config('search').name, 'search')
