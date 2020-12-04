from django.urls import path
from . import views

urlpatterns = [
    # Main Movie Logic
    path('', views.recApp, name="rec"),
]