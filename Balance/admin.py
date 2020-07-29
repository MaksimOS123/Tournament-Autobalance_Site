from django.contrib import admin
from Balance.models import UserProfile
from Balance.models import TournamentModel
from Balance.models import CheckedTournament

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TournamentModel)
admin.site.register(CheckedTournament)