from django.urls import path;
from .views import homePage,registerView,loginView,logoutView
urlpatterns=[
    path("",homePage),
    path("register/",registerView),
    path("login/",loginView),
    path("logout/",logoutView),

]