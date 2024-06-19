from django.contrib import admin
from app_final.models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)



class TripAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Trip, TripAdmin)


