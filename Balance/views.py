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


@login_required
def profile_edit(request):
    context = f_m.get_base_context(request)
    context['title'] = 'Edit profile'
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name
    context['email'] = request.user.email
    context['username'] = request.user

    user = User.objects.filter(username=request.user)[0]
    if request.method == 'POST':
        if request.POST.get('username', False):
            if user.username != request.POST.get('username'):
                user.username = request.POST.get('username')
                user.save()
                context['success'] = 'The username change is successful'
        if request.POST.get('email', False):
            if user.email != request.POST.get('email'):
                user.email = request.POST.get('email')
                user.save()
                context['success'] = 'The email change is successful'
        if request.POST.get('first_name', False) and request.POST.get('last_name', False):
            if user.first_name != request.POST.get('first_name') or user.last_name != request.POST.get('last_name'):
                user.first_name, user.last_name = request.POST.get('first_name'), request.POST.get('last_name')
                user.save()
                context['success'] = 'The name change is successful'
        if request.POST.get('old_pswd', False):
            if user.check_password(request.POST.get('old_pswd')):
                if request.POST.get('new_pswd') == request.POST.get('conf_pswd'):
                    user.set_password(request.POST.get('new_pswd'))
                    user.save()
                    context['success'] = 'The password change is successful'
                else:
                    context['error'] = "New passwords don't match"
            else:
                context['error'] = 'The old password is invalid'

    return render(request, 'profile_edit.html', context)



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