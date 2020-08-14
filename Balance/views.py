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
from pathlib import Path


# Main

def index_page(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = "Main page"

    return render(request, 'index.html', context)


# Log and Reg

def sign_up(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

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


# Profile

@login_required
def profile(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Edit profile'

    user = User.objects.filter(username=request.user)[0]
    this_user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
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

        if request.FILES:
            profile_form = UserPhoto(instance=this_user, data=request.POST, files=request.FILES)
            if profile_form.is_valid():
                if UserProfile.objects.get(user=request.user).photo != 'no_photo.jpg':
                    image1 = str(Path.cwd()) + '/media/' + str(context['photo'])
                    os.remove(image1)
                profile_form.save()
                context['photo'] = UserProfile.objects.get(user=request.user).photo
                context['success'] = 'The image change is successful'
            else:
                profile_form = UserPhoto(instance=this_user)
        else:
            profile_form = UserPhoto(instance=this_user)
    else:
        profile_form = UserPhoto(instance=this_user)

    context['profile_form'] = profile_form

    return render(request, 'profile/profile.html', context)


@login_required()
def profile_pass(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Edit profile'

    user = User.objects.filter(username=request.user)[0]

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

    return render(request, 'profile/profile_pass.html', context)


@login_required()
def profile_statistics(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Edit profile'

    user = User.objects.filter(username=request.user)[0]

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

    return render(request, 'profile/profile_statistics.html', context)


@login_required()
def profile_integrations(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    user = UserProfile.objects.get(user=request.user)
    context['twitch'] = user.twitch
    context['steam'] = user.steam
    context['youtube'] = user.youtube
    context['discord'] = user.discord
    context['discord_server'] = user.discord_server
    context['discord_server_tournament'] = user.discord_server_tournament

    if request.method == 'POST':
        if request.POST.get('twitch') or request.POST.get('twitch') == '':
            user.twitch = request.POST.get('twitch')
        if request.POST.get('youtube') or request.POST.get('youtube') == '':
            user.youtube = request.POST.get('youtube')
        if request.POST.get('discord') or request.POST.get('discord') == '':
            user.discord = request.POST.get('discord')
        if request.POST.get('discord_server') or request.POST.get('discord_server') == '':
            user.discord_server = request.POST.get('discord_server')
        if request.POST.get('discord_server_tournament') or request.POST.get('discord_server_tournament') == '':
            user.discord_server_tournament = request.POST.get('discord_server_tournament')

        user.save()
        return HttpResponseRedirect(request.path)

    return render(request, 'profile/profile_integrations.html', context)


def user_page(request, user_id):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

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

    return render(request, 'profile/user_page.html', context)


# Tournament

def tournament(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

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
    context['end_date'] = tr.end_date
    context['end_tine'] = tr.end_time
    context['members_count'] = tr.members_count
    context['type'] = tr.type
    context['fortype'] = tr.formattype

    players = []
    for i in range(len(tr.userprofile_set.all())):
        players.append(tr.userprofile_set.all()[i].user)
    context['players'] = players

    return render(request, 'tournaments/tournament.html', context)


@login_required()
def my_tournaments(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'My Tournaments'

    tournaments = UserProfile.objects.get(user=request.user).tournaments.all()
    list_of_tournaments = []
    for i in tournaments:
        t = TournamentModel.objects.get(ref=i)
        if not t.archive:
            list_of_tournaments.append(i)

    if len(list_of_tournaments) < len(tournaments):
        context['archives'] = True
        if len(tournaments) - len(list_of_tournaments) == 1:
            context['archives_count'] = '1 tournament archived'
        else:
            context['archives_count'] = '{} tournaments archived'.format(len(tournaments) - len(list_of_tournaments))

    context['tournaments'] = list_of_tournaments

    return render(request, 'tournaments/my_tournaments.html', context)


@login_required()
def archives(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tournaments = UserProfile.objects.get(user=request.user).tournaments.all()
    list_of_tournaments = []
    for i in tournaments:
        t = TournamentModel.objects.get(ref=i)
        if t.archive:
            list_of_tournaments.append(i)

    context['tournaments'] = list_of_tournaments
    context['title'] = "Archives"

    return render(request, 'tournaments/archives.html', context)


@login_required()
def create_tournament(request):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Create Tournament'
    context['errors'] = []

    if request.method == 'POST':
        f = TournamentForm(request.POST)

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
            ed = request.POST.get('end_date')
            et = request.POST.get('end_time')
            tp = request.POST.get('inputType')
            frm = request.POST.get('inputFormat')

            tournament = TournamentModel.objects.create(creator=c, ref=ref, title=t, description=d,
                                                        rules=r, full_rules=fr, prizes=p, date=dt,
                                                        time=tm, schedule=sc, contacts=cn, end_date=ed, end_time=et,
                                                        type=tp, formattype=frm)
            tournament.save()
            tournament.userprofile_set.add(UserProfile.objects.get(user=request.user))

            context['form'] = f
            return HttpResponseRedirect('/console/{}/'.format(ref))
        else:
            context['form'] = f
    else:
        f = TournamentForm()
        context['form'] = f

    date = datetime.datetime.today()
    context['date'] = date.strftime("%Y-%m-%d")

    return render(request, 'tournaments/create_tournament.html', context)


# Console

@login_required()
def console_tournament(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref
    context['public'] = tr.public
    context['archive'] = tr.archive

    if request.method == 'POST':
        if request.POST.get('publish'):
            tr.public = not tr.public
            tr.save()
            return HttpResponseRedirect('/console/{}/'.format(ref))

        if request.POST.get('archive'):
            tr.archive = not tr.archive
            tr.save()
            return HttpResponseRedirect('/console/{}/'.format(ref))

    return render(request, 'tournaments/console_tournament.html', context)


@login_required()
def console_general(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    return render(request, 'console/console_general.html', context)


@login_required()
def console_participant(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    return render(request, 'console/console_participant.html', context)


@login_required()
def console_fields(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    return render(request, 'console/console_fields.html', context)


@login_required()
def console_streams(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)
    user = UserProfile.objects.get(user=request.user)
    if user.twitch:
        context['Twitch'] = True
        context['URLTwitch'] = user.twitch
    if user.youtube:
        context['Youtube'] = True
        context['URLYoutube'] = user.youtube

    context['title'] = tr.title
    context['ref'] = ref

    return render(request, 'console/console_streams.html', context)


@login_required()
def console_permissions(request, ref):
    context = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    return render(request, 'console/console_permissions.html', context)
