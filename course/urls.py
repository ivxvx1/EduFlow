from django.urls import path
from . import views 

urlpatterns = [
    path('', views.user_login, name='login'),
    path('index/', views.index, name='index'), 
    path('about/', views.about, name='about'),  
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('Calendar/', views.Calendar, name='Calendar'),
    path('reviews/', views.reviews, name='reviews'),
    path('library/', views.library, name='library'),
    path('courses_table/', views.courses_table, name='courses_table'), 
    path('courses_report/', views.course_report, name='course_report'),
]
