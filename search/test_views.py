from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import Post
from shoppingcart.models import Item
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import pytz


class SearchAppViewsTest(TestCase):
    """Class for testing search app views"""

    """Set up the user, post, draft and item for testing"""
    def setUp(self):
        self.credentials = {
            'username': 'username1',
            'password': 'random'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.post = Post(author=self.user, title='post', likes_total=100,
                         text='this is a post', published_date=datetime.datetime(2019, 9, 4, tzinfo=pytz.UTC))
        self.post.save()
        self.draft = Post(author=self.user, title='draft', likes_total=100,
                          text='this is a draft')
        self.draft.save()
        self.shirt = Item(title='Shirt', price=300.0, category='Shirts', label='primary', slug='random-slug', description='shirt')
        self.shirt.image = SimpleUploadedFile(name='BE266_rose_top.jpg',
                                              content=open('/home/ubuntu/environment/ecommerce/media/random.jpg', 'rb').read(),
                                              content_type='image/jpeg')
        self.shirt.save()

    """Test 'GET' search posts view (same as post list view)"""
    def test_get_search_posts_view(self):
        response = self.client.get('/forum/search_posts/')
        self.assertEqual(response.context['post_list_count'], 0)
        self.assertTemplateUsed(response, 'forum/post_list.html')

    """Test search announcements(posts) 'POST' success ('len(search_text) > 1')"""
    def test_search_announcements_post_success_search_text_length_more_than_one(self):
        response = self.client.post('/forum/search_posts/', {'posts': 'blog post'})
        self.assertEqual(response.context['post_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')
        
    """Test search announcements(posts) 'POST' success ('len(search_text) = 1')"""
    def test_search_announcements_post_success_search_text_length_one(self):
        response = self.client.post('/forum/search_posts/', {'posts': 'p'})
        self.assertEqual(response.context['post_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')

    """Test post results JSON response used for AJAX request ('len(search_text) > 1')"""
    def test_posts_results_search_text_length_more_than_one(self):
        response = self.client.post('/forum/posts_results/post/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'post': 1}])
        
    """Test post results JSON response used for AJAX request ('len(search_text) = 1')"""
    def test_posts_results_search_text_length_one(self):
        response = self.client.post('/forum/posts_results/p/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'post': 1}])

    """
    Test 'GET' search drafts view (same as post list view - includes
    posts that don't have a published date)
    """
    def test_get_search_drafts_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/search_drafts/')
        self.assertEqual(response.context['draft_list_count'], 0)
        self.assertTemplateUsed(response, 'forum/post_list.html')

    """Test search drafts 'POST' success ('len(search_text) > 1')"""
    def test_search_drafts_post_success_search_text_length_more_than_one(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/search_drafts/', {'drafts': 'draft'})
        self.assertEqual(response.context['draft_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')

    """Test search drafts 'POST' success ('len(search_text) = 1')"""
    def test_search_drafts_post_success_search_text_length_one(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/search_drafts/', {'drafts': 'd'})
        self.assertEqual(response.context['draft_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')

    """Test drafts results JSON response used for AJAX request ('len(search_text) = 1')"""
    def test_drafts_results_search_text_length_one(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/drafts_results/d/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'draft': 2}])

    """Test drafts results JSON response used for AJAX request ('len(search_text) > 1')"""
    def test_drafts_results_search_text_length_more_than_one(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/drafts_results/draft/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'draft': 2}])

    """Test 'GET' search products view (same as home view)"""
    def test_get_search_products_view(self):
        response = self.client.get('/shoppingcart/search_products/')
        self.assertEqual(response.context['item_list_count'], 0)
        self.assertTemplateUsed(response, 'shoppingcart/home.html')

    """Test search products 'POST' success ('len(search_text) > 1')"""
    def test_search_products_post_success_search_text_length_more_than_one(self):
        response = self.client.post('/shoppingcart/search_products/', {'item_search': 'shirt'})
        self.assertEqual(response.context['item_list_count'], 1)
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    """Test search products 'POST' success ('len(search_text) = 1')"""
    def test_search_products_post_success(self):
        response = self.client.post('/shoppingcart/search_products/', {'item_search': 's'})
        self.assertEqual(response.context['item_list_count'], 1)
        self.assertTemplateUsed(response, 'shoppingcart/home.html')

    """Test products results JSON response used for AJAX request ('len(search_text) > 1')"""
    def test_products_results_search_text_length_more_than_one(self):
        response = self.client.post('/shoppingcart/products_results/shirt/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'Shirt': 'random-slug'}])
        
    """Test products results JSON response used for AJAX request ('len(search_text) = 1')"""
    def test_products_results_search_text_length_one(self):
        response = self.client.post('/shoppingcart/products_results/s/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'Shirt': 'random-slug'}])

    """Test filter products by tags"""
    def test_filter_by_tags(self):
        response = self.client.post('/shoppingcart/filter_by_tags/belts/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
