from rest_framework import serializers
from .models import Olympiad, Question, Submission


class QuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.ChoiceField(choices=[
        ('text', 'Text Answer'),
        ('code', 'Code'),
        ('multiple_choice', 'Multiple Choice'),
    ])

    class Meta:
        model = Question
        fields = ['id', 'olympiad', 'text', 'question_type', 'max_score', 'hint', 'mc_options', 'mc_answer']
        read_only_fields = ['mc_answer']  # Hide correct answer from users


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('user', 'score', 'submitted_at', 'is_cheating', 'attempt_number')


class OlympiadSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Olympiad
        fields = '__all__'
