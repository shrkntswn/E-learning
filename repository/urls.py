from django.urls import path
from .import views

app_name = 'repository'
urlpatterns = [
    path('login/', views.userLogin, name='userLogin'),
    path('registration/', views.registration, name='registration'),
    path('home/', views.home, name='home'),
    path('create/playlist', views.createPlaylist, name='createPlaylist'),
    path('playlist/video/<str:id>', views.ViewVideoPlaylist, name='ViewVideoPlaylist'),
    path('create/video/<str:id>', views.CreateVideoPlaylist, name='CreateVideoPlaylist'),
    #path('teacher/registration', views.teacherRegistration, name='teacherRegistration'),
]
