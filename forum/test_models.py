from django.test import TestCase
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.models import User


class TestForumModels(TestCase):
    """Class for testing forum models"""

    """Set up the user, post and comment for testing"""
    def setUp(self):
        user = User.objects.create_user('goagl', 'hello@yahoo.com', 'randompassword')
        user.save()
        self.post = Post(author=user, title='post')
        self.post.save()
        self.comment = Comment(author=user, post=self.post, reply=None, approved_comment=True)
        self.comment.save()

    """Test '__str__' return for post and post publish method (published_date)"""
    def test_post_publish_and_title(self):
        self.post.publish()
        self.assertEqual(self.post.published_date.day, timezone.now().day)
        self.assertEqual(str(self.post), 'post')

    """
    Test post approve comment queryset equals 'approved_comments'
    queryset (approved_comment=True)
    """
    def test_post_approve_comments(self):
        approved_comments = list(Comment.objects.filter(approved_comment=True))
        self.assertQuerysetEqual(self.post.approve_comments(), [repr(comment) for comment in approved_comments])

    """
    Test post comments excluding replies queryset equals
    'comments_excluding_replies' queryset (reply=None)
    """
    def test_post_comments_excluding_replies(self):
        comments_excluding_replies = list(Comment.objects.filter(reply=None))
        self.assertQuerysetEqual(self.post.comments_excluding_replies(), [repr(comment) for comment in comments_excluding_replies])

    """Test post absolute url"""
    def test_post_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/forum/post/1/')

    """Test post total likes count"""
    def test_post_likes_count(self):
        user = User.objects.get(username='goagl')
        self.post.likes.add(user)
        self.post.save()
        self.assertEqual(self.post.total_likes(), 1)

    """Test approve method for comment and comment absolute url"""
    def test_comment_approve_and_absolute_url(self):
        user = User.objects.get(username='goagl')
        new_comment = Comment(author=user, post=self.post, reply=None, approved_comment=False)
        new_comment.save()
        new_comment.approve()
        self.assertEqual(new_comment.approved_comment, True)
        self.assertEqual(new_comment.get_absolute_url(), '/forum/')
