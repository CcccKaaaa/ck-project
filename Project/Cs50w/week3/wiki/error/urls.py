from django.urls import path
from . import views

app_name = "error"
urlpatterns = [
    path("<str:entry>", views.index, name="index")
]