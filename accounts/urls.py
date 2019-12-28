from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('addIssue', views.add_issue, name='addIssue'),
    path('addSol', views.add_sol, name='addSol'),
    path('addList', views.add_list, name='addList'),

]
