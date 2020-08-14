from django.contrib import admin
from Balance.models import UserProfile
from Balance.models import TournamentModel

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TournamentModel)