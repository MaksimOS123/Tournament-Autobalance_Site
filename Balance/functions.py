from django.contrib.auth.models import User
from Balance.models import UserProfile
from django.http import HttpResponseRedirect
import time


def get_base_context(request):
    context = {}
    if request.user.is_authenticated:
        context['first_name'] = request.user.first_name
        context['last_name'] = request.user.last_name
        context['email'] = request.user.email
        context['username'] = request.user

        if not UserProfile.objects.filter(user=request.user).exists():
            UserProfile(user=request.user).save()

        context['photo'] = UserProfile.objects.get(user=request.user).photo
        if UserProfile.objects.get(user=request.user).dark_mode:
            context['mode_main'] = 'dark_main.css'
            context['mode_profile'] = 'dark_profile.css'
            context['mode_console'] = 'dark_console.css'
            context['mode_img'] = 'dark.jpg'
        else:
            context['mode_main'] = 'main.css'
            context['mode_profile'] = 'profile.css'
            context['mode_console'] = 'console.css'
            context['mode_img'] = 'light.jpg'

    return context


def check_dark(request):
    if request.method == 'POST':
        if request.POST.get('dark'):
            user_mode = UserProfile.objects.get(user=request.user)
            user_mode.dark_mode = not user_mode.dark_mode
            user_mode.save()
            return True

    return False


def is_existing_user(users_list, username):
    for user in users_list:
        if user.username == username:
            return True

    return False
