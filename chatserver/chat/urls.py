from django.contrib import admin
from django.urls import path , re_path
from .views import ThreadView, InboxView


app_name = "chat"

urlpatterns = [
    path("", InboxView.as_view()),
    path("<str:username>/", ThreadView.as_view()),
]
