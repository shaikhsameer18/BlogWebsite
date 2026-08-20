from django.test import TestCase

from blogwebsite.models import Category, Post


class BlogViewTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            title='Coding', description='Code stuff', url='coding', image='category/test.png'
        )
        self.post = Post.objects.create(
            title='Test Post', content='<p>Hello world</p>', url='test-post', cat=self.cat, image='post/test.png'
        )

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_about_page_loads(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_loads(self):
        response = self.client.get(f'/blogs/{self.post.url}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_detail_missing_slug_returns_404(self):
        response = self.client.get('/blogs/does-not-exist')
        self.assertEqual(response.status_code, 404)

    def test_category_page_loads(self):
        response = self.client.get(f'/category/{self.cat.url}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_category_missing_slug_returns_404(self):
        response = self.client.get('/category/does-not-exist')
        self.assertEqual(response.status_code, 404)
