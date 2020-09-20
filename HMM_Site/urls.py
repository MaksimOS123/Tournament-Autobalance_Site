"""HMM_Site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from Balance import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main
    path('', views.index_page, name="main"),

    # Log and Reg
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('reg/', views.sign_up, name="register"),

    # Profile
    path('profile/', views.profile, name="profile"),
    path('profile/security/', views.profile_pass, name="profile_security"),
    path('profile/statistics/', views.profile_statistics, name="profile_statistics"),
    path('profile/integrations/', views.profile_integrations, name="profile_integrations"),
    path('user/<int:user_id>/', views.user_page, name="user_page"),

    # Tournaments
    path('create_tournament/', views.create_tournament, name="create_tournament"),
    path('tournament/<str:ref>/', views.tournament, name="tournament"),
    path('tournaments/', views.my_tournaments, name="my_tournaments"),
    path('archives/', views.archives, name="archives"),

    # Console Tournaments
    path('console/<str:ref>/', views.console_tournament, name="console_tournament"),
    path('console/<str:ref>/general/', views.console_general, name="console_general"),
    path('console/<str:ref>/participant/', views.console_participant, name="console_participant"),
    path('console/<str:ref>/fields/', views.console_fields, name="console_fields"),
    path('console/<str:ref>/streams/', views.console_streams, name="console_streams"),
    path('console/<str:ref>/partners_streams/', views.console_partners_streams, name="console_partners_streams"),
    path('console/<str:ref>/permissions/', views.console_permissions, name="console_permissions"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
