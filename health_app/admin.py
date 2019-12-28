from django.contrib import admin
from .models import Issues, Solutions, Trainees_health_issues, Solution_list


class IssuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'solve_ability')
    list_display_links = ('code',)
    list_filter = ('solve_ability',)
    list_editable = ('solve_ability',)
    search_fields = ('code', 'description',)
    list_per_page = 25


class SolutionsAdmin(admin.ModelAdmin):
    list_display = ('code',)
    list_display_links = ('code',)
    search_fields = ('code', 'description',)
    list_per_page = 25


class Solution_listAdmin(admin.ModelAdmin):
    list_display = ('issue', 'solution', 'is_valid',)
    list_display_links = ('issue',)
    list_editable = ('solution', 'is_valid',)
    list_filter = ('issue',)
    search_fields = ('issue', 'solution',)
    list_per_page = 25


class Trainees_health_issuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainee', 'issue', 'healed', 'issue_date',)
    list_display_links = ('trainee',)
    list_filter = ('trainee', 'healed',)
    list_editable = ('healed',)
    search_fields = ('trainee', 'issue', 'issue_date',)
    list_per_page = 25


admin.site.register(Issues, IssuesAdmin)
admin.site.register(Solutions, SolutionsAdmin)
admin.site.register(Solution_list, Solution_listAdmin)
admin.site.register(Trainees_health_issues, Trainees_health_issuesAdmin)
