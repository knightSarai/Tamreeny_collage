from django.urls import path
from . import views
from health_app.views import *

app_name = 'health_app'

urlpatterns = [
    path('level', views.level, name='level'),
    path('injured', views.injured, name='injured'),
    path('shape', views.shape, name='shape'),
    path('elite', views.elite, name='elite'),
    path('list', views.health_list, name='list'),
    path('search', views.issue_search, name='issueSearch'),
    #     path('<int:id>/', IssueDetailView.as_view(), name='issue-details'),
    path('<int:issue_id>/', views.Issue_details, name='issue_detail'),
    path('<int:id>/delete/', IssueDeleteView.as_view(), name='issue-delete'),
    path('trainee/<int:id>/', TraineeIssueDetailView.as_view(),
         name='trainee-issue-details'),
    path('trainee/<int:id>/delete/', TraineeIssueDeleteView.as_view(),
         name='trainee-issue-delete'),
    path('update', views.update_issue, name='update'),
    path('healed', views.healed_update, name='healed'),


]
