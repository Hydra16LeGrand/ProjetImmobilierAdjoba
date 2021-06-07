from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Utilisateur)
admin.site.register(Bien)
admin.site.register(Terrain)
admin.site.register(Maison)
admin.site.register(Agent)