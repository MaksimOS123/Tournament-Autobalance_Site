from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Streamers(models.Model):
    platform = models.TextField(default='')
    language = models.TextField(default='')
    link = models.URLField(default='')


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
    official_streamer_youtube = models.URLField(default='')
    partners_streamers_twitch = models.ForeignKey(Streamers, on_delete=models.CASCADE, default=1)
    partners_streamers_youtube = models.TextField(default='')

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
    discord_server = models.URLField(default='')
    discord_server_tournament = models.URLField(default='')
    dark_mode = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/', blank=True, default='no_photo.jpg')
    tournaments = models.ManyToManyField(TournamentModel)


'''class Course(models.Model):
    name = models.CharField(max_length=30)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)'''
