from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import Post
from shoppingcart.models import Item
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import pytz


class SearchAppViewsTest(TestCase):
    
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
    
    def test_get_search_posts_view(self):
        response = self.client.get('/forum/search_posts/')
        self.assertEqual(response.context['post_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')
        
    def test_search_announcements_post_success(self):
        response = self.client.post('/forum/search_posts/', {'posts': 'blog post'})
        self.assertEqual(response.context['post_list_count'], 0)
        self.assertTemplateUsed(response, 'forum/post_list.html')
    
    def test_posts_results(self):
        response = self.client.post('/forum/posts_results/post/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'post': 1}])
        
    def test_get_search_drafts_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/search_drafts/')
        self.assertEqual(response.context['draft_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')
    
    def test_search_drafts_post_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/search_drafts/', {'drafts': 'draft'})
        self.assertEqual(response.context['draft_list_count'], 1)
        self.assertTemplateUsed(response, 'forum/post_list.html')

    def test_drafts_results(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/drafts_results/draft/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'draft': 2}])
    
    def test_get_search_products_view(self):
        response = self.client.get('/shoppingcart/search_products/')
        self.assertEqual(response.context['item_list_count'], 1)
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_search_products_post_success(self):
        response = self.client.post('/shoppingcart/search_products/', {'item_search': 'shirt'})
        self.assertEqual(response.context['item_list_count'], 1)
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_products_results(self):
        response = self.client.post('/shoppingcart/products_results/shirt/')
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{'Shirt': 'random-slug'}])
        
    def test_filter_by_dresses(self):
        response = self.client.post('/shoppingcart/filter/dresses/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_shoes(self):
        response = self.client.post('/shoppingcart/filter/shoes/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_suits(self):
        response = self.client.post('/shoppingcart/filter/suits/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_veils(self):
        response = self.client.post('/shoppingcart/filter/veils/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_rings(self):
        response = self.client.post('/shoppingcart/filter/rings/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_flowers(self):
        response = self.client.post('/shoppingcart/filter/flowers/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_hair_accessories(self):
        response = self.client.post('/shoppingcart/filter/hair_accessories/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_shirts(self):
        response = self.client.post('/shoppingcart/filter/shirts/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_purses(self):
        response = self.client.post('/shoppingcart/filter/purses/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_belts(self):
        response = self.client.post('/shoppingcart/filter/belts/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
        
    def test_filter_by_tags(self):
        response = self.client.post('/shoppingcart/filter_by_tags/belts/')
        self.assertTemplateUsed(response, 'shoppingcart/home.html')
