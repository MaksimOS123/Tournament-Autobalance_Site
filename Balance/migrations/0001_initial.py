# Generated by Django 3.0.6 on 2020-07-19 11:42

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
            name='TournamentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(default='', max_length=500)),
                ('title', models.CharField(default='', max_length=200)),
                ('description', models.TextField()),
                ('rules', models.CharField(default='', max_length=1500)),
                ('full_rules', models.TextField()),
                ('prizes', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('schedule', models.TextField()),
                ('contacts', models.TextField()),
                ('end_registration', models.DateTimeField()),
                ('members_count', models.CharField(default='0', max_length=500)),
                ('type', models.CharField(choices=[('F', 'Free agents'), ('P', 'Pair Registration'), ('T', 'Teams')], default='F', max_length=1)),
                ('formattype', models.CharField(choices=[('S', 'Default format'), ('R', 'Round Robin')], default='S', max_length=1)),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, default='no_photo.jpg', upload_to='images/')),
                ('tournaments', models.ManyToManyField(to='Balance.TournamentModel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckedTournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Balance.TournamentModel')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
