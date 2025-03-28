from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path(r"login/", views.LoginView.as_view()),
    path(r"message/", views.MessageView.as_view()),
    path(r"credential/", views.CredentialView.as_view())
]
