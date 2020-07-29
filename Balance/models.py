from django.contrib.auth.models import User
from django.db import models

# Create your models here.


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
    end_registration = models.DateTimeField()
    public = models.BooleanField(default=False)

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
    photo = models.ImageField(upload_to='images/', blank=True, default='no_photo.jpg')
    tournaments = models.ManyToManyField(TournamentModel)


class CheckedTournament(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    tournament_id = models.ForeignKey(to=TournamentModel, on_delete=models.CASCADE, default="")



'''class Course(models.Model):
    name = models.CharField(max_length=30)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)'''