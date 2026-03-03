"""
URL configuration for school_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from users.views import UserViewSet
from olympiads.views import OlympiadViewSet
from news.views import AnnouncementViewSet
from profiles.views import ProfileViewSet
from olympiads.views import QuestionViewSet, SubmissionViewSet
from chat.views import ChatMessageViewSet
from school_platform import admin_urls

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'olympiads', OlympiadViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'chatmessages', ChatMessageViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('school_platform.admin_urls', namespace='custom_admin')),
    path('auth/', include('users.urls')),
    path('olympiads/', include('olympiads.urls')),
    path('news/', include('news.urls')),
    path('chat/', include('chat.urls')),
    path('profiles/', include('profiles.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
