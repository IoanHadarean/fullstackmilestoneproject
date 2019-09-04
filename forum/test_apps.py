from django.apps import apps
from django.test import TestCase
from forum.apps import ForumConfig


class ForumAppConfigTest(TestCase):
    """Class for testing forum app config"""

    def test_forum_app_config(self):
        self.assertEqual(ForumConfig.name, 'forum')
        self.assertEqual(apps.get_app_config('forum').name, 'forum')
