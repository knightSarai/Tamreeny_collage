from django.urls import path
from . import views

urlpatterns = [
    path('<int:trainee_id>', views.index, name='predict'),
]
