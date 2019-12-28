from django.contrib import admin

from .models import Trainees, Physical_attribute, Shape_state, Workouts


class TraineesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',
                    'roll_date', 'trainer', 'shape', 'is_active', 'health_issue', 'future_elite')
    list_display_links = ('id', 'trainer')
    list_filter = ('trainer', 'level', 'roll_date', 'shape', 'is_active')
    list_editable = ('is_active', 'shape', 'is_active',
                     'health_issue', 'future_elite')
    search_fields = ('name', 'note', 'address',
                     'phone', 'level', 'is_active')
    list_per_page = 25


class Physical_attributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainee', 'date',)
    list_display_links = ('id', 'trainee')
    list_filter = ('trainee', 'date',)
    search_fields = ('trainee',)
    list_per_page = 25


class Shape_stateAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainee', 'date',)
    list_display_links = ('id', 'trainee')
    list_filter = ('trainee', 'date',)
    search_fields = ('trainee',)
    list_per_page = 25


class WorkoutsAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainee', 'date',)
    list_display_links = ('id', 'trainee')
    list_filter = ('trainee', 'date',)
    search_fields = ('trainee', 'content')
    list_per_page = 25


admin.site.register(Trainees, TraineesAdmin)
admin.site.register(Physical_attribute, Physical_attributeAdmin)
admin.site.register(Shape_state, Shape_stateAdmin)
admin.site.register(Workouts, WorkoutsAdmin)
