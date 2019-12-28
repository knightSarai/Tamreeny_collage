from django.contrib import admin
from .models import *


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainee', 'inactive', 'active')


class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'date', 'vlaue')
    list_filter = ('trainee', 'date')


admin.site.register(ShapeData)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Progress)
admin.site.register(Health)
admin.site.register(PredictionResult, PredictionResultAdmin)
