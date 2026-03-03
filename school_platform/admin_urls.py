from django.urls import path
from django.views.decorators.http import require_http_methods
from . import admin_views

app_name = 'custom_admin'

urlpatterns = [
    path('', admin_views.admin_dashboard, name='dashboard'),
    path('users/', admin_views.users_list, name='users'),
    path('users/edit/<int:user_id>/', admin_views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', admin_views.delete_user, name='delete_user'),
    path('olympiads/', admin_views.olympiads_list, name='olympiads'),
    path('olympiads/create/', admin_views.create_olympiad, name='create_olympiad'),
    path('olympiads/edit/<int:olympiad_id>/', admin_views.edit_olympiad, name='edit_olympiad'),
    path('olympiads/delete/<int:olympiad_id>/', admin_views.delete_olympiad, name='delete_olympiad'),
    path('questions/<int:olympiad_id>/', admin_views.questions_list, name='questions'),
    path('questions/create/<int:olympiad_id>/', admin_views.create_question, name='create_question'),
    path('submissions/', admin_views.submissions_list, name='submissions'),
    path('logs/', admin_views.audit_logs, name='audit_logs'),
]
