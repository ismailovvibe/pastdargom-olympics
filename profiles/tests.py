from django.test import TestCase
from django.urls import reverse


class ProfileTests(TestCase):
    def test_profile(self):
        # anonymous users are redirected, authenticated users see their profile
        from users.models import User
        user = User.objects.create_user(username='testuser', password='Testpass123!', email='test@example.com')
        self.client.login(username='testuser', password='Testpass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        # context should include our statistics
        self.assertIn('total_submissions', response.context)
        self.assertIn('correct_submissions', response.context)
        # email appears in rendered page
        self.assertContains(response, 'test@example.com')

    def test_scoreboard_requires_login(self):
        resp = self.client.get(reverse('scoreboard'))
        self.assertRedirects(resp, '/auth/register/?next=' + reverse('scoreboard'))
        # logging in makes it accessible
        from users.models import User
        u = User.objects.create_user(username='sco', password='Testpass123!')
        self.client.login(username='sco', password='Testpass123!')
        resp2 = self.client.get(reverse('scoreboard'))
        self.assertEqual(resp2.status_code, 200)

    def test_edit_profile_get_and_post(self):
        from users.models import User
        user = User.objects.create_user(username='edituser', password='Testpass123!')
        self.client.login(username='edituser', password='Testpass123!')
        # GET form
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        # POST update (no file to avoid image validation issues)
        response = self.client.post(reverse('edit_profile'), {'bio': 'hello'})
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.profile.bio, 'hello')
        # avatar should still be empty by default
        self.assertFalse(user.profile.avatar)


class ProfileAPITests(TestCase):
    def setUp(self):
        from users.models import User
        from .models import Profile
        self.user = User.objects.create_user(username='profuser', password='Testpass123!')
        Profile.objects.create(user=self.user)
        self.client.login(username='profuser', password='Testpass123!')

    def test_list(self):
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, 200)
