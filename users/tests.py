from django.test import TestCase
from django.urls import reverse
from .models import User


class UserViewsTests(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_counts(self):
        # Create minimal data to verify counts appear
        from olympiads.models import Olympiad, Question, Submission
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='homeuser', password='Testpass123!')
        o = Olympiad.objects.create(title='Test', subject='Math', start_time='2025-01-01T00:00Z', end_time='2025-01-02T00:00Z')
        q = Question.objects.create(olympiad=o, text='t', question_type='text', max_score=1)
        Submission.objects.create(question=q, user=user, answer_text='foo')
        response = self.client.get(reverse('home'))
        # counts should show values (at least 1)
        self.assertContains(response, '1')

    def test_register_login(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='testuser')
        self.assertTrue(user)


class UserAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='Testpass123!')
        self.client.login(username='apiuser', password='Testpass123!')

    def test_list_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)


class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='resetuser', email='test@example.com', password='Testpass123!')

    def test_reset_flow(self):
        response = self.client.post(reverse('password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)  # redirect to done
