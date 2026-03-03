from django.contrib import admin
from .models import Olympiad, Question, Submission


from .forms import QuestionForm

class QuestionInline(admin.TabularInline):
    model = Question
    form = QuestionForm
    fields = ['text', 'question_type', 'max_score', 'hint', 'mc_options', 'mc_answer']
    extra = 1


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'start_time', 'end_time', 'status', 'duration_minutes']
    list_filter = ['status', 'subject']
    inlines = [QuestionInline]
    actions = ['open_olympiad', 'close_olympiad']

    def open_olympiad(self, request, queryset):
        queryset.update(status=Olympiad.OPEN)
    open_olympiad.short_description = "Mark selected as open"

    def close_olympiad(self, request, queryset):
        queryset.update(status=Olympiad.CLOSED)
    close_olympiad.short_description = "Mark selected as closed"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'olympiad', 'question_type', 'max_score']
    list_filter = ['question_type', 'olympiad']
    search_fields = ['text']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'score', 'attempt_number', 'submitted_at', 'is_cheating']
    list_filter = ['is_cheating', 'question__olympiad', 'submitted_at']
    search_fields = ['user__username']
    readonly_fields = ['submitted_at']
