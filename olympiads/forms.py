from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        qtype = cleaned.get('question_type')
        options = cleaned.get('mc_options')
        answer = cleaned.get('mc_answer')
        if qtype == Question.TYPE_MULTIPLE_CHOICE:
            if not options or len(options) < 2:
                raise forms.ValidationError('Multiple choice questions require at least two options.')
            if answer is None or answer < 0 or answer >= len(options):
                raise forms.ValidationError('Please select a valid answer index.')
        else:
            cleaned['mc_options'] = []
            cleaned['mc_answer'] = None
        return cleaned