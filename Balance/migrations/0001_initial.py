# Generated by Django 3.1.2 on 2020-12-05 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Streamers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(default='')),
                ('platform', models.CharField(choices=[('T', 'Twitch'), ('Y', 'Youtube')], default='T', max_length=1)),
                ('language', models.CharField(choices=[('ru', 'Russian'), ('en', 'English'), ('RN', 'Russian+English')], default='en', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(default='', max_length=500)),
                ('title', models.CharField(default='', max_length=200)),
                ('description', models.TextField(default='')),
                ('rules', models.CharField(default='', max_length=1500)),
                ('full_rules', models.TextField(default='')),
                ('prizes', models.TextField(default='')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('schedule', models.TextField(default='')),
                ('contacts', models.TextField(default='')),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('public', models.BooleanField(default=False)),
                ('archive', models.BooleanField(default=False)),
                ('official_streamer_twitch', models.URLField(default='')),
                ('official_streamer_language', models.TextField(default='')),
                ('official_streamer_youtube', models.URLField(default='')),
                ('discord_server', models.URLField(default='')),
                ('members_count', models.CharField(default='0', max_length=500)),
                ('type', models.CharField(choices=[('F', 'Free agents'), ('P', 'Pair Registration'), ('T', 'Teams')], default='F', max_length=1)),
                ('formattype', models.CharField(choices=[('S', 'Default format'), ('R', 'Round Robin')], default='S', max_length=1)),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('partners_streamers', models.ManyToManyField(to='Balance.Streamers')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitch', models.URLField(default='')),
                ('steam', models.URLField(default='')),
                ('youtube', models.URLField(default='')),
                ('discord', models.TextField(default='')),
                ('discord_server_tournament', models.URLField(default='')),
                ('wins', models.IntegerField(default=0)),
                ('loses', models.IntegerField(default=0)),
                ('kills', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('damage', models.IntegerField(default=0)),
                ('repair', models.IntegerField(default=0)),
                ('t_bombs', models.IntegerField(default=0)),
                ('d_bombs', models.IntegerField(default=0)),
                ('dark_mode', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, default='no_photo.jpg', upload_to='images/')),
                ('bg_user', models.CharField(choices=[('00', 'default'), ('01', 'stars'), ('02', 'cycle'), ('03', 'ground'), ('04', 'winter'), ('05', 'bang'), ('06', 'cybercity'), ('07', 'ink'), ('08', 'black_hole'), ('09', 'cyber'), ('10', 'forest')], default='00', max_length=2)),
                ('tournaments', models.ManyToManyField(to='Balance.TournamentModel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
