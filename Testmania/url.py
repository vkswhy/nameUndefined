from django.urls import path;
from .views import homePage,registerView,loginView,logoutView,createTestView,takeTestView,profile
urlpatterns=[
    path("",homePage),
    path("register/",registerView),
    path("login/",loginView),
    path("logout/",logoutView),
    path("createtest/",createTestView),
    path("taketest/",takeTestView),
    path("profile/",profile)
]