from django.urls import path
from .views import HomeView, CiudadanoView


urlpatterns= [
    path("", HomeView.as_view()),
    path("ciudadano/", CiudadanoView.as_view()),
]
