from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Comment
from .factories import UserFactory, PostFactory, CommentFactory

class ProjectTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = UserFactory(username='testni_korisnik', password='password123')

    def test_post_model_str(self):
        """Testira vraća li model ispravan naziv (string representation)"""
        post = PostFactory(title="Naslov posta")
        self.assertEqual(str(post), "Naslov posta")

    def test_homepage_view(self):
        """Testira učitava li se naslovnica i vide li se postovi"""
        
        PostFactory.create_batch(3)
        
        response = self.client.get(reverse('post_list'))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.context['posts']), 3)

    def test_post_detail_view(self):
        """Testira radi li pojedinačni prikaz posta"""
        post = PostFactory(title="Detaljni naslov", content="Neki sadržaj")
        
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detaljni naslov")
        self.assertContains(response, "Neki sadržaj")

    def test_create_post_authenticated(self):
        """Testira može li logirani korisnik stvoriti post"""
        self.client.force_login(self.user) 
        
        data = {
            'title': 'Novi testni post',
            'content': 'Sadržaj novog posta'
        }
        
        response = self.client.post(reverse('post_create'), data)
        
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(Post.objects.filter(title='Novi testni post').exists())