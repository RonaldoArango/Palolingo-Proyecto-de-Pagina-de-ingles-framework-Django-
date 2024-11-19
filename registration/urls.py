"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app1 import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('audioCore/',views.pagina_audio, name='pagina'),
    path('reconocer_audio/', views.reconocer_audio, name='reconocer_audio'),
    path('home/',views.home_view,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('accounts/', include('allauth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('oauth2/', include('social_django.urls', namespace='social')),
    path('corrector/', views.correct_text, name='correct_text'),
    path('foro/',views.foro,name='foro'),
    path('addInForum/',views.addInForum,name='addInForum'),
    path('addInDiscussion/',views.addInDiscussion,name='addInDiscussion'),
    path('input/', views.input_word, name='input_word'),
    path('display/<str:word>/', views.display_word, name='display_word'),
    path('temas/', views.temas, name='temas'),
    path('temas/present_simple/', views.present_simple, name='present_simple'),
    path('temas/past_simple/', views.past_simple, name='past_simple'),
    path('temas/future_simple/', views.future_simple, name='future_simple'),
    path('temas/present_continuous/', views.present_continuous, name='present_continuous'),
    path('temas/past_continuous/', views.past_continuous, name='past_continuous'),
    path('marcar_aprendido/<str:tema>/', views.marcar_aprendido, name='marcar_aprendido'),
    path('start/', views.start_quiz_view, name='start'),
    path('get-questions/start', views.get_questions, {'is_start': True}, name='get-questions'),
    path('get-questions', views.get_questions, {'is_start': False}, name='get-questions'),
    path('get-answer', views.get_answer, name='get-answer'),
    path('get-finish', views.get_finish, name='get-finish'),
    path('ejercicios_present_simple/', views.present_simple_exercises, name='ejercicios_present_simple'),
]

from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Bienvenido al Corrector de Textos</h1><a href="/corrector/">Ir al Corrector</a>')

