from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Streamers(models.Model):
    link = models.URLField(default='')

    platform_type = (
        ('T', 'Twitch'),
        ('Y', 'Youtube'),
    )

    language_type = (
        ('ru', 'Russian'),
        ('en', 'English'),
        ('RN', 'Russian+English'),
    )

    platform = models.CharField(max_length=1, choices=platform_type, default='T')
    language = models.CharField(max_length=2, choices=language_type, default='en')

    def __int__(self):
        return self.id


class TournamentModel(models.Model):
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    ref = models.CharField(max_length=500, default='')

    title = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    rules = models.CharField(max_length=1500, default='')
    full_rules = models.TextField(default='')
    prizes = models.TextField(default='')
    date = models.DateField()
    time = models.TimeField()
    schedule = models.TextField(default='')
    contacts = models.TextField(default='')
    end_date = models.DateField()
    end_time = models.TimeField()

    public = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

    official_streamer_twitch = models.URLField(default='')
    official_streamer_language = models.TextField(default='')
    official_streamer_youtube = models.URLField(default='')
    partners_streamers = models.ManyToManyField(Streamers)

    discord_server = models.URLField(default='')

    members_count = models.CharField(max_length=500, default='0')

    TYPES = (
        ('F', 'Free agents'),
        ('P', 'Pair Registration'),
        ('T', 'Teams'),
    )

    FormatTYPES = (
        ('S', 'Default format'),
        ('R', 'Round Robin'),
    )

    type = models.CharField(max_length=1, choices=TYPES, default='F')
    formattype = models.CharField(max_length=1, choices=FormatTYPES, default='S')

    def __str__(self):
        return self.ref


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    twitch = models.URLField(default='')
    steam = models.URLField(default='')
    youtube = models.URLField(default='')
    discord = models.TextField(default='')
    discord_server_tournament = models.URLField(default='')

    dark_mode = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/', blank=True, default='no_photo.jpg')

    BACKGROUDS = (
        ('00', 'default'),
        ('01', 'stars'),
        ('02', 'cycle'),
        ('03', 'ground'),
        ('04', 'winter'),
        ('05', 'bang'),
        ('06', 'cybercity'),
        ('07', 'ink'),
        ('08', 'black_hole'),
        ('09', 'cyber'),
        ('10', 'forest'),
    )

    bg_user = models.CharField(max_length=2, choices=BACKGROUDS, default='00')

    tournaments = models.ManyToManyField(TournamentModel)


'''class Course(models.Model):
    name = models.CharField(max_length=30)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)'''
