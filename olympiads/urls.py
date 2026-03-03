from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_olympiads, name='olympiads_list'),
    path('<int:olympiad_id>/questions/', views.olympiad_questions, name='olympiad_questions'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('submission/<int:submission_id>/result/', views.submission_result, name='submission_result'),
]
