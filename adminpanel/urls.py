from django.urls import path
from . import views

urlpatterns =[
    path("login",views.login,name="login"),
    path("register", views.register, name="register"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("calender", views.calender, name="calender"),
    path("maps", views.maps, name="maps"),
    path("register", views.register, name="register"),
    path("datasets", views.datasets, name="datasets"),
    path("settings", views.settings, name="settings"),
    path("dashboard", views.dashboard,name="dashboard"),
    path("index", views.index, name="index"),
]