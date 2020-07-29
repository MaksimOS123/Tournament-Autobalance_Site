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
    path('', views.index_page, name="main"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('reg/', views.sign_up, name="register"),
    path('profile/', views.profile, name="profile"),
    path('user/<int:user_id>/', views.user_page, name="user_page"),
    path('create_tournament/', views.create_tournament, name="create_tournament"),
    path('tournament/<str:ref>/', views.tournament, name="tournament"),
    path('tournaments/', views.my_tournaments, name="my_tournaments"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
