from django.contrib.auth.models import User
from Balance.models import UserProfile


def get_base_context(request):
    context = {}
    if request.user.is_authenticated:
        context['email'] = request.user.email
        context['username'] = request.user
        context['id'] = request.user.id

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

    platform = str(request.META['HTTP_USER_AGENT'])
    if "Android" in platform or "iPhone" in platform:
        mobile = True
    else:
        mobile = False

    return context, mobile


def check_dark(request):
    if request.method == 'POST':
        if request.POST.get('dark'):
            user_mode = UserProfile.objects.get(user=request.user)
            user_mode.dark_mode = not user_mode.dark_mode
            user_mode.save()
            return True

    return False


def get_links_for_console(context, tr):
    if tr.official_streamer_twitch:
        a = tr.official_streamer_twitch.split('/')
        context['Twitch'] = a[len(a)-1]
    if tr.official_streamer_youtube:
        a = tr.official_streamer_youtube.split('/')
        context['Youtube'] = a[len(a)-1]

    if tr.official_streamer_language:
        context['Language'] = tr.official_streamer_language
    else:
        context['Language'] = 'Language'

    tr.save()

    return context


def get_language_stream(answer, tr):

    if 'inputLanguage' in answer:
        print('test')
        if answer['inputLanguage'][0] == '1':
            tr.official_streamer_language = 'Russian'
        elif answer['inputLanguage'][0] == '3':
            tr.official_streamer_language = 'Russian+English'
        else:
            tr.official_streamer_language = 'English'
    elif not tr.official_streamer_language:
        tr.official_streamer_language = 'English'

    tr.save()


def edit_links(answer, tr, user):
    if '1' not in answer['inputPlatform']:
        tr.official_streamer_twitch = ''
    if '2' not in answer['inputPlatform']:
        tr.official_streamer_youtube = ''

    if len(answer['inputPlatform']) < 2 and len(answer['inputPlatform']) != 0:
        if answer['inputPlatform'][0] == '1':
            tr.official_streamer_twitch = 'https://www.twitch.tv/' + answer['link'][0]
            if not user.twitch:
                user.twitch = 'https://www.twitch.tv/' + answer['link'][0]
        elif answer['inputPlatform'][0] == '2':
            tr.official_streamer_youtube = 'https://www.youtube.com/channel/' + answer['link'][0]
            if not user.youtube:
                user.youtube = 'https://www.youtube.com/channel/' + answer['link'][0]
    else:
        if answer['inputPlatform'][0] == '1':
            tr.official_streamer_twitch = 'https://www.twitch.tv/' + answer['link'][0]
            if not user.twitch:
                user.twitch = 'https://www.twitch.tv/' + answer['link'][0]
        elif answer['inputPlatform'][0] == '2':
            tr.official_streamer_youtube = 'https://www.youtube.com/channel/' + answer['link'][0]
            if not user.youtube:
                user.youtube = 'https://www.youtube.com/channel/' + answer['link'][0]
        if answer['inputPlatform'][1] == '1':
            tr.official_streamer_twitch = 'https://www.twitch.tv/' + answer['link'][1]
            if not user.twitch:
                user.twitch = 'https://www.twitch.tv/' + answer['link'][1]
        elif answer['inputPlatform'][1] == '2':
            tr.official_streamer_youtube = 'https://www.youtube.com/channel/' + answer['link'][1]
            if not user.youtube:
                user.youtube = 'https://www.youtube.com/channel/' + answer['link'][1]

    tr.save()
    user.save()


def is_existing_user(users_list, username):
    for user in users_list:
        if user.username == username:
            return True

    return False
