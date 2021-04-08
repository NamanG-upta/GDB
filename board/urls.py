from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("help", views.go, name="help"),
	path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('startbtn/', views.startbtn, name="startbtn"),
    path('stopbtn/', views.stopbtn, name="stopbtn"),
]