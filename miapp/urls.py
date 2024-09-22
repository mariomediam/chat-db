from django.urls import path
from .views import HomeView, CiudadanoView, QueryView


urlpatterns= [
    path("", HomeView.as_view()),
    path("ciudadano/", CiudadanoView.as_view()),
    path("query/", QueryView.as_view())
]
