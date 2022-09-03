from django.urls import path
from . import views

app_name = "random_page"
urlpatterns = [
    path("", views.random_page, name="random"),
]
