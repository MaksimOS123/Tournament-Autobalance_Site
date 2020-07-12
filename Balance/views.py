from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

import Balance.functions as f_m
from Balance.forms import SignInForm
# Create your views here.


def index_page(request):
    context = f_m.get_base_context(request)
    context['title'] = "Main page"

    return render(request, 'index.html', context)


def sign_up(request):
    context = f_m.get_base_context(request)
    context['title'] = 'Регистрация'
    context['errors'] = []

    if request.method == 'POST':
        f = SignInForm(request.POST)

        if f.is_valid():
            u_n = f.data['user_name']
            u_fn = f.data['user_first_name']
            u_ln = f.data['user_last_name']
            u_em = f.data['user_email']
            u_pw = f.data['password']
            u_pw_c = f.data['password_conf']

            if not f_m.is_existing_user(User.objects.all(), u_n):
                if u_pw == u_pw_c:
                    new_user = User.objects.create_user(username=u_n, first_name=u_fn, last_name=u_ln, email=u_em,
                                                        password=u_pw)
                    new_user.save()
                    return HttpResponseRedirect('/login/')
                else:
                    context['errors'].append("Введенные пароли не совпадают")
            else:
                context['errors'].append("Пользователь с таким логином уже существует")

            context['form'] = f
        else:
            context['form'] = f
    else:
        f = SignInForm()
        context['form'] = f

    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    context = f_m.get_base_context(request)
    context['username'] = request.user
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name
    context['email'] = request.user.email

    return render(request, 'profile.html', context)


def user_page(request, user_id):
    context = f_m.get_base_context(request)
    user = User.objects.get(id=user_id)
    context['username'] = user
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['email'] = user.email
    if request.user == user:
        return HttpResponseRedirect('/profile/')

    return render(request, 'user_page.html', context)