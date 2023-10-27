from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

admin.site.register(Game)
admin.site.register(Characters)
admin.site.register(Enemies)
admin.site.register(Equipment)
admin.site.register(Spells)
admin.site.register(Quests)
admin.site.register(Locations)
admin.site.register(MewGame)
admin.site.register(Users, UserAdmin)
admin.site.register(UserEquipment)
admin.site.register(UserSpells)
admin.site.register(UserQuests)
admin.site.register(UserProfile)
admin.site.register(Playthroughs)
admin.site.register(Tags)
admin.site.register(OtherImages)
