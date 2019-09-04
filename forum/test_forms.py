from django.test import TestCase
from .models import Post, Comment
from .forms import PostForm, PostEditForm, CommentForm, CommentEditForm
from django.contrib.auth.models import User


class TestForumForms(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'username1',
            'password': 'random'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.post = Post(author=self.user, title='post', text='this is a post')
        self.post.save()
        self.comment =  Comment(author=self.user, post=self.post, text='comment')
        
    def test_post_edit_form(self):
        form_params = {'title': 'edited post', 'text': 'this is an edited post'}
        post_edit_form = PostEditForm(self.post, form_params)
        self.assertEqual(post_edit_form.fields['title'].initial, 'post')
        self.assertEqual(post_edit_form.fields['text'].initial, 'this is a post')
        
    def test_comment_edit_form(self):
        form_params = {'text': 'edited comment'}
        comment_edit_form = CommentEditForm(self.comment, form_params)
        self.assertEqual(comment_edit_form.fields['text'].initial, 'comment')
