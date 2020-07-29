import os
import datetime
import hashlib

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import LANGUAGE_SESSION_KEY

import Balance.functions as f_m
from Balance.forms import SignInForm
from Balance.forms import TournamentForm
# Create your views here.
from Balance.forms import UserPhoto
from Balance.models import UserProfile
from Balance.models import TournamentModel


def index_page(request):
    context = f_m.get_base_context(request)
    context['title'] = "Main page"

    return render(request, 'index.html', context)


def tournament(request, ref):
    context = f_m.get_base_context(request)
    tr = TournamentModel.objects.get(ref=ref)
    context['title'] = tr.title
    context['description'] = tr.description
    context['rules'] = tr.rules
    context['full_rules'] = tr.full_rules
    context['prizes'] = tr.prizes
    context['date'] = tr.date
    context['time'] = tr.time
    context['schedule'] = tr.schedule
    context['contacts'] = tr.contacts
    context['end_registration'] = tr.end_registration
    context['members_count'] = tr.members_count
    context['type'] = tr.type
    context['fortype'] = tr.formattype

    players = []
    for i in range(len(tr.userprofile_set.all())):
        players.append(tr.userprofile_set.all()[i].user)
    context['players'] = players

    return render(request, 'tournament.html', context)


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


@login_required()
def my_tournaments(request):
    context = f_m.get_base_context(request)
    context['title'] = 'My Tournaments'
    context['username'] = request.user

    if not UserProfile.objects.filter(user=request.user).exists():
        UserProfile(user=request.user).save()

    if UserProfile.objects.get(user=request.user).photo:
        context['photo'] = UserProfile.objects.get(user=request.user).photo

    context['tournaments'] = UserProfile.objects.get(user=request.user).tournaments.all()

    return render(request, 'my_tournaments.html', context)


@login_required()
def create_tournament(request):
    context = f_m.get_base_context(request)
    context['title'] = 'Create Tournament'
    context['errors'] = []
    context['username'] = request.user

    if not UserProfile.objects.filter(user=request.user).exists():
        UserProfile(user=request.user).save()

    if UserProfile.objects.get(user=request.user).photo:
        context['photo'] = UserProfile.objects.get(user=request.user).photo

    if request.method == 'POST':
        f = TournamentForm(request.POST)
        print(f)

        if f.is_valid():
            c = request.user
            DateTimeNow = str(datetime.datetime.now())
            ref = str(hashlib.md5(DateTimeNow.encode()).hexdigest())
            t = f.data['title']
            d = f.data['description']
            r = f.data['rules']
            fr = f.data['full_rules']
            p = f.data['prizes']
            dt = f.data['date']
            tm = f.data['time']
            sc = f.data['schedule']
            cn = f.data['contacts']
            ern = request.POST.get('end_registration')
            tp = request.POST.get('inputType')
            frm = request.POST.get('inputFormat')

            tournament = TournamentModel.objects.create(creator=c, ref=ref, title=t, description=d,
                                                        rules=r, full_rules=fr, prizes=p, date=dt,
                                                        time=tm, schedule=sc, contacts=cn, end_registration=ern, type=tp, formattype=frm)
            tournament.save()
            tournament.userprofile_set.add(UserProfile.objects.get(user=request.user))

            context['form'] = f
            return HttpResponseRedirect('/tournament/{}/'.format(ref))
        else:
            context['form'] = f
    else:
        f = TournamentForm()
        context['form'] = f

    return render(request, 'create_tournament.html', context)


@login_required
def profile(request):
    context = f_m.get_base_context(request)
    context['username'] = request.user
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name
    context['email'] = request.user.email

    #print(UserProfile.objects.get(user=request.user).tournaments.all())

    '''
    UserProfile.objects.get(user=request.user).tournaments.all()[0].title
    
    test = TournamentModel.objects.get(ref="just test")
    print(test.userprofile_set.all()[0].user)
    
    for i in range(python.student_set.count()):
        print(python.student_set.all()[i].user)'''

    if not UserProfile.objects.filter(user=request.user).exists():
        UserProfile(user=request.user).save()

    if UserProfile.objects.get(user=request.user).photo:
        context['photo'] = UserProfile.objects.get(user=request.user).photo

    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    context = f_m.get_base_context(request)
    context['title'] = 'Edit profile'
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name
    context['email'] = request.user.email
    context['username'] = request.user

    if not UserProfile.objects.filter(user=request.user).exists():
        UserProfile(user=request.user).save()

    if UserProfile.objects.get(user=request.user).photo:
        context['photo'] = UserProfile.objects.get(user=request.user).photo

    user = User.objects.filter(username=request.user)[0]
    this_user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.GET.get('ref'))
        if request.POST.get('username', False):
            if user.username != request.POST.get('username'):
                if not User.objects.filter(username=request.POST.get('username')).exists():
                    user.username = request.POST.get('username')
                    user.save()
                    context['success'] = 'The login change is successful'
                else:
                    context['error'] = 'This login is already taken'
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

        if request.FILES:
            profile_form = UserPhoto(instance=this_user, data=request.POST, files=request.FILES)
            if profile_form.is_valid():
                if UserProfile.objects.get(user=request.user).photo:
                    image1 = 'C:/test/HMM_Site/media/' + str(context['photo'])
                    os.remove(image1)
                profile_form.save()
                context['photo'] = UserProfile.objects.get(user=request.user).photo
            else:
                profile_form = UserPhoto(instance=this_user)
        else:
            profile_form = UserPhoto(instance=this_user)
    else:
        profile_form = UserPhoto(instance=this_user)

    context['profile_form'] = profile_form

    return render(request, 'profile_edit.html', context)



def user_page(request, user_id):
    context = f_m.get_base_context(request)
    user = User.objects.get(id=user_id)
    context['username'] = user
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['email'] = user.email
    if UserProfile.objects.filter(user=user).exists():
        if UserProfile.objects.get(user=user).photo:
            context['photo'] = UserProfile.objects.get(user=user).photo

    if request.user == user:
        return HttpResponseRedirect('/profile/')

    return render(request, 'user_page.html', context)