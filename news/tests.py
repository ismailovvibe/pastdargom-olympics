from django.test import TestCase
from django.urls import reverse
from .models import Announcement


class NewsTests(TestCase):
    def test_list(self):
        # anonymous should be redirected to registration
        response = self.client.get(reverse('news_list'))
        self.assertRedirects(response, '/auth/register/?next=' + reverse('news_list'))
        # after login the page loads
        from users.models import User
        u = User.objects.create_user(username='foo', password='Testpass123!')
        self.client.login(username='foo', password='Testpass123!')
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)


class NewsAPITests(TestCase):
    def setUp(self):
        from .models import Announcement
        Announcement.objects.create(title='Title', content='Some text')
        from users.models import User
        self.user = User.objects.create_user(username='newsuser', password='Testpass123!')
        self.client.login(username='newsuser', password='Testpass123!')

    def test_list(self):
        response = self.client.get('/api/announcements/')
        self.assertEqual(response.status_code, 200)

    def test_react(self):
        # must be logged in
        ann = Announcement.objects.first()
        response = self.client.post(reverse('react_announcement', args=[ann.id]), {'type': 'like'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('likes', data)
        # toggling
        response2 = self.client.post(reverse('react_announcement', args=[ann.id]), {'type': 'like'})
        self.assertEqual(response2.status_code, 200)
