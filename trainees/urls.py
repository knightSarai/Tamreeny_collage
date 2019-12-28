from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='trainees'),
    path('<int:trainee_id>', views.trainee, name='trainee'),
    path('search', views.search, name='search'),
    path('note', views.note, name='note'),
    path('traineeIssue', views.trainee_issue, name='addTraineeIssue'),
    path('workouts/<int:trainee_id>', views.workouts_list, name='workouts'),
    path('add/workouts', views.add_workout, name='addWorkout'),
    path('edit/workouts', views.edit_workout, name='editWorkout'),
    path('classifier', views.physical_attribute, name='physical_attribute'),
    path('active', views.active, name='active'),

]
