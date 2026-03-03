from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('react/<int:announcement_id>/', views.react_announcement, name='react_announcement'),
]
