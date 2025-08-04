from django.urls import path
from . import views
from accounts.views import DashboardView   

app_name = "courses"

urlpatterns = [
    path('categories/', views.all_categories, name='all_categories'),
    path('tags/', views.all_tags, name='all_tags'),
    path('category/<slug:slug>/', views.category_courses, name='category_courses'),
    path('tag/<slug:slug>/', views.tag_courses, name='tag_courses'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('', views.course_list, name='course_list'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

 ]
