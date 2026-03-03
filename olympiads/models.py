from django.db import models
from django.conf import settings


class Olympiad(models.Model):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'
    STATUS_CHOICES = [OPEN, IN_PROGRESS, CLOSED]

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[(s, s) for s in STATUS_CHOICES], default=OPEN)
    # duration in minutes
    duration_minutes = models.IntegerField(default=120)

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE_TEXT = 'text'
    TYPE_CODE = 'code'
    TYPE_MULTIPLE_CHOICE = 'multiple_choice'
    QUESTION_TYPES = [
        (TYPE_TEXT, 'Text Answer'),
        (TYPE_CODE, 'Code'),
        (TYPE_MULTIPLE_CHOICE, 'Multiple Choice'),
    ]

    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TYPE_TEXT)
    max_score = models.IntegerField(default=0)
    hint = models.TextField(blank=True, null=True)
    # for multiple choice
    mc_options = models.JSONField(default=list, blank=True)  # ['option1', 'option2', ...]
    mc_answer = models.IntegerField(blank=True, null=True)  # index of correct answer

    def __str__(self):
        return f"Q{self.id} ({self.get_question_type_display()}) for {self.olympiad.title}"

    def clean(self):
        # custom validation to avoid mismatched options
        from django.core.exceptions import ValidationError
        super().clean()
        if self.question_type == Question.TYPE_MULTIPLE_CHOICE:
            if not self.mc_options or len(self.mc_options) < 2:
                raise ValidationError('Multiple choice questions require at least two options')
            if self.mc_answer is None or not (0 <= self.mc_answer < len(self.mc_options)):
                raise ValidationError('Please provide a valid answer index')
        else:
            # clear MC fields when not applicable
            self.mc_options = []
            self.mc_answer = None


class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # allow text or code depending on question type
    answer_text = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    mc_choice = models.IntegerField(blank=True, null=True)  # index of selected option for MC
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_cheating = models.BooleanField(default=False)
    attempt_number = models.IntegerField(default=1)  # 1st, 2nd, 3rd attempt...

    def __str__(self):
        return f"Submission {self.id} by {self.user.username} (attempt {self.attempt_number})"

    def evaluate(self):
        # placeholder for automatic judging (e.g., python code execution)
        if self.question.question_type == Question.TYPE_MULTIPLE_CHOICE:
            # MC: check if choice matches answer
            if self.mc_choice == self.question.mc_answer:
                self.score = self.question.max_score
            else:
                self.score = 0
        elif self.question.question_type == Question.TYPE_CODE:
            # Code: naive eval: accept if code contains "print("
            if self.code and "print(" in self.code:
                self.score = self.question.max_score
            else:
                self.score = 0
        elif self.question.question_type == Question.TYPE_TEXT:
            # Text: require admin review or keyword matching
            # for now, give partial credit
            self.score = self.question.max_score // 2 if self.answer_text else 0
        self.save()
