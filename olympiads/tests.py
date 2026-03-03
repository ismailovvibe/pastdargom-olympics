from django.test import TestCase
from django.urls import reverse


class OlympiadTests(TestCase):
    def test_list(self):
        # now login required; anonymous user should be sent to register
        response = self.client.get(reverse('olympiads_list'))
        self.assertRedirects(response, '/auth/register/?next=' + reverse('olympiads_list'))
        # after login we see the page
        from users.models import User
        user = User.objects.create_user(username='temp', password='Testpass123!')
        self.client.login(username='temp', password='Testpass123!')
        response = self.client.get(reverse('olympiads_list'))
        self.assertEqual(response.status_code, 200)

    def test_questions_login_required(self):
        from .models import Olympiad
        olymp = Olympiad.objects.create(title='Temp2', subject='p', start_time='2025-01-01T00:00Z', end_time='2025-01-02T00:00Z')
        response = self.client.get(reverse('olympiad_questions', args=[olymp.id]))
        self.assertRedirects(response, '/auth/register/?next=' + reverse('olympiad_questions', args=[olymp.id]))

    def test_question_page_submission(self):
        # GET should redirect when not logged in
        from .models import Question, Olympiad
        response = self.client.get(reverse('question_detail', args=[1]))
        self.assertRedirects(response, '/auth/register/?next=' + reverse('question_detail', args=[1]))
        # ensure view handles form POST correctly for each type when authenticated
        from users.models import User
        u = User.objects.create_user(username='viewuser', password='Testpass123!')
        self.client.login(username='viewuser', password='Testpass123!')
        olymp = Olympiad.objects.create(title='Temp', subject='s', start_time='2025-01-01T00:00Z', end_time='2025-01-02T00:00Z')
        # create questions for each type
        q_text = Question.objects.create(olympiad=olymp, text='what?', question_type='text', max_score=2)
        q_code = Question.objects.create(olympiad=olymp, text='print(1)', question_type='code', max_score=3)
        q_mc = Question.objects.create(olympiad=olymp, text='choose', question_type='multiple_choice', max_score=4, mc_options=['a','b'], mc_answer=1)
        # text submission
        resp = self.client.post(reverse('question_detail', args=[q_text.id]), {'answer_text': 'foo'})
        self.assertEqual(resp.status_code, 302)
        # code submission
        resp = self.client.post(reverse('question_detail', args=[q_code.id]), {'code': 'print(2)'})
        self.assertEqual(resp.status_code, 302)
        # mc submission
        resp = self.client.post(reverse('question_detail', args=[q_mc.id]), {'mc_choice': '1'})
        self.assertEqual(resp.status_code, 302)
        
        # submitting without any answer should show error message
        resp = self.client.post(reverse('question_detail', args=[q_text.id]), {})
        self.assertEqual(resp.status_code, 200)  # stays on page
        self.assertContains(resp, "Iltimos, javob yozing")


class OlympiadAPITests(TestCase):
    def setUp(self):
        from .models import Olympiad, Question
        self.olym = Olympiad.objects.create(title='Test', subject='math', start_time='2026-01-01T00:00Z', end_time='2026-01-01T01:00Z')
        self.code_q = Question.objects.create(olympiad=self.olym, text='print(1)', question_type='code', max_score=10)
        self.mc_q = Question.objects.create(
            olympiad=self.olym, 
            text='What is 2+2?', 
            question_type='multiple_choice', 
            max_score=5,
            mc_options=['3', '4', '5'],
            mc_answer=1  # index 1 = '4'
        )
        from users.models import User
        self.user = User.objects.create_user(username='apiuser2', password='Testpass123!')
        self.client.login(username='apiuser2', password='Testpass123!')

    def test_list(self):
        response = self.client.get('/api/olympiads/')
        self.assertEqual(response.status_code, 200)

    def test_question_submission(self):
        # submit code for question
        data = {'question': self.code_q.id, 'code': 'print(42)'}
        response = self.client.post('/api/submissions/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['score'], 10)

    def test_mc_submission_correct(self):
        # submit correct MC answer
        data = {'question': self.mc_q.id, 'mc_choice': 1}  # correct
        response = self.client.post('/api/submissions/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['score'], 5)

    def test_mc_submission_wrong(self):
        # submit wrong MC answer
        data = {'question': self.mc_q.id, 'mc_choice': 0}  # wrong
        response = self.client.post('/api/submissions/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['score'], 0)

    def test_cheating_detection(self):
        data = {'question': self.code_q.id, 'code': 'print(42)'}
        resp1 = self.client.post('/api/submissions/', data)
        resp2 = self.client.post('/api/submissions/', data)
        self.assertEqual(resp2.status_code, 201)
        self.assertTrue(resp2.json()['is_cheating'])
        self.assertEqual(resp2.json()['score'], 0)

    def test_profile_score_update(self):
        # make a clean submission and check profile score increments
        from profiles.models import Profile
        data = {'question': self.code_q.id, 'code': 'print(42)'}
        resp = self.client.post('/api/submissions/', data)
        self.assertEqual(resp.status_code, 201)
        # force refresh from DB
        from .models import Submission
        submission = Submission.objects.latest('id')
        self.assertEqual(submission.score, 10)
        self.assertFalse(submission.is_cheating)
        profile = Profile.objects.get(user=self.user)
        # score should have been incremented by signal
        self.assertEqual(profile.score, 10)
