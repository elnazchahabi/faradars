from django.urls import path
from . import views

app_name = "instructors"

urlpatterns = [
    path('<str:username>/', views.instructor_profile, name='profile'),
]
