from django.urls import path
from . import views

app_name = "create"
urlpatterns = [
    path("", views.index, name="index")
]