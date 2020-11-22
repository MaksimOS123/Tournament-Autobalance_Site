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
from Balance.models import Streamers
from pathlib import Path


# Main

def index_page(request):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = "Main page"

    tournaments = []

    for i in range(1, TournamentModel.objects.all().last().id+1):
        tour = TournamentModel.objects.get(id=i)
        if tour.public:
            tournaments.append(tour)

    context['tournaments'] = tournaments

    if mobile:
        return render(request, 'mobile/index.html', context)
    else:
        return render(request, 'index.html', context)


# Log and Reg

def sign_up(request):
    context, mobile = f_m.get_base_context(request)
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

    if mobile:
        return render(request, 'mobile/registration/register.html', context)
    else:
        return render(request, 'registration/register.html', context)


# Profile

@login_required
def profile(request):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Edit profile'

    backgrounds = ['bang',
                    'cybercity',
                    'cycle',
                    'ground',
                    'ink',
                    'stars',
                    'winter',
                    'black_hole',
                    'cyber',
                    'forest']

    code_bg = {
        'bang': '05',
        'cybercity': '06',
        'cycle': '02',
        'ground': '03',
        'ink': '07',
        'stars': '01',
        'winter': '04',
        'black_hole': '08',
        'cyber': '09',
        'forest': '10',
    }

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

        if request.POST.get('old_pswd', False):
            if user.check_password(request.POST.get('old_pswd')):
                if request.POST.get('new_pswd'):
                    user.set_password(request.POST.get('new_pswd'))
                    user.save()
                    context['success'] = 'The password change is successful'
            else:
                context['error'] = 'The old password is invalid'

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

        if request.POST.get('bg', False):
            this_user.bg_user = code_bg[request.POST.get('bg')]
            this_user.save()

    else:
        profile_form = UserPhoto(instance=this_user)

    context['profile_form'] = profile_form
    context['backgrounds'] = backgrounds
    context['bg_user'] = this_user.get_bg_user_display()

    if mobile:
        return render(request, 'mobile/profile/profile.html', context)
    else:
        return render(request, 'profile/profile.html', context)


@login_required()
def profile_statistics(request):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Edit profile'

    user = User.objects.filter(username=request.user)[0]

    return HttpResponseRedirect('/profile/')


@login_required()
def profile_integrations(request):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    user = UserProfile.objects.get(user=request.user)
    context['twitch'] = user.twitch
    context['steam'] = user.steam
    context['youtube'] = user.youtube
    context['discord'] = user.discord
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

    if mobile:
        return render(request, 'mobile/profile/profile_integrations.html', context)
    else:
        return render(request, 'profile/profile_integrations.html', context)


def user_page(request, user_id):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    user = User.objects.get(id=user_id)
    if UserProfile.objects.filter(user=user).exists():
        this_user = UserProfile.objects.get(user=user)

    context['username'] = user
    context['email'] = user.email

    if this_user.photo:
        context['photo'] = UserProfile.objects.get(user=user).photo

    context['bg'] = this_user.get_bg_user_display()

    if mobile:
        return render(request, 'mobile/profile/user_page.html', context)
    else:
        return render(request, 'profile/user_page.html', context)


# Tournament

def tournament(request, ref):
    context, mobile = f_m.get_base_context(request)
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
    context['end_time'] = tr.end_time
    context['members_count'] = tr.members_count
    context['type'] = tr.type
    context['fortype'] = tr.formattype

    '''players = []
    for i in range(len(tr.userprofile_set.all())):
        players.append(tr.userprofile_set.all()[i].user)
    context['players'] = players'''

    context['discord_server'] = tr.discord_server
    context['creator'] = tr.creator

    if mobile:
        return render(request, 'mobile/tournaments/tournament.html', context)
    else:
        return render(request, 'tournaments/tournament.html', context)


@login_required()
def my_tournaments(request):
    context, mobile = f_m.get_base_context(request)
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

    if mobile:
        return render(request, 'mobile/tournaments/my_tournaments.html', context)
    else:
        return render(request, 'tournaments/my_tournaments.html', context)


@login_required()
def archives(request):
    context, mobile = f_m.get_base_context(request)
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

    if mobile:
        return render(request, 'mobile/tournaments/archives.html', context)
    else:
        return render(request, 'tournaments/archives.html', context)


@login_required()
def create_tournament(request):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    context['title'] = 'Create Tournament'
    context['errors'] = []

    if request.method == 'POST':
        f = TournamentForm(request.POST)
        user = UserProfile.objects.get(user=request.user)

        if f.is_valid():
            c = request.user
            date_time_now = str(datetime.datetime.now())
            ref = str(hashlib.md5(date_time_now.encode()).hexdigest())
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

            tour = TournamentModel.objects.create(creator=c, ref=ref, title=t, description=d,
                                                  rules=r, full_rules=fr, prizes=p, date=dt,
                                                  time=tm, schedule=sc, contacts=cn, end_date=ed, end_time=et,
                                                  type=tp, formattype=frm)

            if user.twitch:
                tour.official_streamer_twitch = user.twitch
            if user.youtube:
                tour.official_streamer_youtube = user.youtube
            if user.discord_server_tournament:
                tour.discord_server = user.discord_server_tournament

            tour.save()
            tour.userprofile_set.add(UserProfile.objects.get(user=request.user))

            context['form'] = f
            return HttpResponseRedirect('/console/{}/'.format(ref))
        else:
            context['form'] = f
    else:
        f = TournamentForm()
        context['form'] = f

    date = datetime.datetime.today()
    context['date'] = date.strftime("%Y-%m-%d")

    if mobile:
        return render(request, 'mobile/tournaments/create_tournament.html', context)
    else:
        return render(request, 'tournaments/create_tournament.html', context)


# Console

@login_required()
def console_tournament(request, ref):
    context, mobile = f_m.get_base_context(request)
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

    if mobile:
        return render(request, 'mobile/tournaments/console_tournament.html', context)
    else:
        return render(request, 'tournaments/console_tournament.html', context)


@login_required()
def console_general(request, ref):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    today = datetime.datetime.today()
    context['today'] = today.strftime("%Y-%m-%d")

    context['title'] = tr.title
    context['creator'] = tr.creator
    context['description'] = tr.description
    context['rules'] = tr.rules
    context['full_rules'] = tr.full_rules
    context['prizes'] = tr.prizes
    context['date'] = str(tr.date)
    context['time'] = str(tr.time)
    context['schedule'] = tr.schedule
    context['contacts'] = tr.contacts
    context['end_date'] = str(tr.end_date)
    context['end_time'] = str(tr.end_time)
    context['discord_server'] = tr.discord_server
    context['formattype'] = tr.formattype
    context['type'] = tr.type
    context['ref'] = ref

    if request.method == 'POST':
        if request.POST.get('title') or request.POST.get('title') == '':
            tr.title = request.POST.get('title')
        if request.POST.get('description') or request.POST.get('description') == '':
            tr.description = request.POST.get('description')
        if request.POST.get('rules') or request.POST.get('rules') == '':
            tr.rules = request.POST.get('rules')
        if request.POST.get('full_rules') or request.POST.get('full_rules') == '':
            tr.full_rules = request.POST.get('full_rules')
        if request.POST.get('prizes') or request.POST.get('prizes') == '':
            tr.prizes = request.POST.get('prizes')
        if request.POST.get('date') or request.POST.get('date') == '':
            tr.date = request.POST.get('date')
        if request.POST.get('time') or request.POST.get('time') == '':
            tr.time = request.POST.get('time')
        if request.POST.get('schedule') or request.POST.get('schedule') == '':
            tr.schedule = request.POST.get('schedule')
        if request.POST.get('contacts') or request.POST.get('contacts') == '':
            tr.contacts = request.POST.get('contacts')
        if request.POST.get('end_date') or request.POST.get('end_date') == '':
            tr.end_date = request.POST.get('end_date')
        if request.POST.get('end_time') or request.POST.get('end_time') == '':
            tr.end_time = request.POST.get('end_time')
        if request.POST.get('discord_server') or request.POST.get('discord_server') == '':
            tr.discord_server = request.POST.get('discord_server')
        if request.POST.get('inputType') or request.POST.get('inputType') == '':
            tr.type = request.POST.get('inputType')
        if request.POST.get('inputFormat') or request.POST.get('inputFormat') == '':
            tr.formattype = request.POST.get('inputFormat')

        tr.save()
        return HttpResponseRedirect(request.path)

    if mobile:
        return render(request, 'mobile/console/console_general.html', context)
    else:
        return render(request, 'console/console_general.html', context)


@login_required()
def console_participant(request, ref):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    if mobile:
        return render(request, 'mobile/console/console_participant.html', context)
    else:
        return render(request, 'console/console_participant.html', context)


@login_required()
def console_fields(request, ref):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    if mobile:
        return render(request, 'mobile/console/console_fields.html', context)
    else:
        return render(request, 'console/console_fields.html', context)


@login_required()
def console_streams(request, ref):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)
    user = UserProfile.objects.get(user=request.user)

    context['title'] = tr.title
    context['ref'] = ref
    context = f_m.get_links_for_console(context, tr)

    if request.method == 'POST':
        if request.POST.get('link') and request.POST.get('inputPlatform'):
            answer = eval(str(request.POST).split('<QueryDict: ')[1].split('>')[0])
            f_m.get_language_stream(answer, tr)
            f_m.edit_links(answer, tr, user)

            return HttpResponseRedirect(request.path)
        else:
            tr.official_streamer_twitch = ''
            tr.official_streamer_youtube = ''
            tr.save()

            return HttpResponseRedirect(request.path)

    if mobile:
        return render(request, 'mobile/console/console_streams.html', context)
    else:
        return render(request, 'console/console_streams.html', context)


@login_required()
def console_partners_streams(request, ref):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)
    user = UserProfile.objects.get(user=request.user)

    streamers = tr.partners_streamers.all()
    for i in range(len(streamers)):
        link = streamers[i].link.split('/')
        if link[len(link)-1]:
            link = link[len(link)-1]
        else:
            link = link[len(link)-2]
        streamers[i].link = link

    context['streamers'] = streamers

    context['title'] = tr.title
    context['ref'] = ref

    if request.method == 'POST':
        if request.POST.get('link') and request.POST.get('inputPlatform'):
            answer = eval(str(request.POST).split('<QueryDict: ')[1].split('>')[0])
            tr.partners_streamers.clear()
            for i in range(len(answer['link'])):
                if answer['inputPlatform'][i] == '1':
                    if 'https://' in answer['link'][i]:
                        a = answer['link'][i].split('/')
                        if a[len(a)-1]:
                            link_now = 'https://twitch.tv/' + a[len(a)-1]
                            link_www_now = 'https://www.twitch.tv/' + a[len(a)-1]
                        else:
                            link_now = 'https://twitch.tv/' + a[len(a) - 2]
                            link_www_now = 'https://www.twitch.tv/' + a[len(a) - 2]
                    else:
                        link_now = 'https://twitch.tv/' + answer['link'][i]
                        link_www_now = 'https://www.twitch.tv/' + answer['link'][i]
                    platform = 'T'
                elif answer['inputPlatform'][i] == '2':
                    if 'https://' in answer['link'][i]:
                        a = answer['link'][i].split('/')
                        if a[len(a)-1]:
                            link_now = 'https://youtube.com/channel/' + a[len(a)-1]
                            link_www_now = 'https://www.youtube.com/channel/' + a[len(a)-1]
                        else:
                            link_now = 'https://youtube.com/channel/' + a[len(a) - 2]
                            link_www_now = 'https://www.youtube.com/channel/' + a[len(a) - 2]
                    else:
                        link_now = 'https://youtube.com/channel/' + answer['link'][i]
                        link_www_now = 'https://www.youtube.com/channel/' + answer['link'][i]
                    platform = 'Y'

                if answer['inputLanguage'][i] == '1':
                    language = 'ru'
                if answer['inputLanguage'][i] == '2':
                    language = 'en'
                if answer['inputLanguage'][i] == '3':
                    language = 'RN'

                if link_now != user.twitch and link_www_now != user.twitch and link_now != user.youtube and link_www_now != user.youtube:
                    tr.partners_streamers.create(link=link_now, language=language, platform=platform)

            return HttpResponseRedirect(request.path)
        else:
            tr.partners_streamers.clear()

            return HttpResponseRedirect(request.path)

    if mobile:
        return render(request, 'mobile/console/console_partners_streams.html', context)
    else:
        return render(request, 'console/console_partners_streams.html', context)


@login_required()
def console_permissions(request, ref):
    context, mobile = f_m.get_base_context(request)
    if f_m.check_dark(request):
        return HttpResponseRedirect(request.path)

    tr = TournamentModel.objects.get(ref=ref)

    context['title'] = tr.title
    context['ref'] = ref

    if mobile:
        return render(request, 'mobile/console/console_permissions.html', context)
    else:
        return render(request, 'console/console_permissions.html', context)
