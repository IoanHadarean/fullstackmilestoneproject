from django.apps import apps
from django.test import TestCase
from forum.apps import ForumConfig


class ForumConfigTest(TestCase):
    """Class for testing forum app config"""

    def test_contact_config(self):
        self.assertEqual(ForumConfig.name, 'forum')
        self.assertEqual(apps.get_app_config('forum').name, 'forum')
