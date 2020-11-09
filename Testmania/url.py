from django.urls import path;
from .views import homePage,register
urlpatterns=[
    path("",homePage),
    path("register/",register),
]