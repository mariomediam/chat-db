from django.shortcuts import render
from rest_framework.views import APIView  
from django.http import JsonResponse  

from miapp.models import CiudadanoModel
from miapp.serializers import CiudadanoSerializer

# Create your views here.
class HomeView(APIView):  

 def get(self, request, format=None):
    return JsonResponse({"message":
    'HOLA MUNDO DESDE DJANGO Y DOCKER', "content":
    'Por Mario Medina'}) 
 
class CiudadanoView(APIView):  
 serializer_class = CiudadanoSerializer

 def get(self, request, format=None):
   cod_ciudadano = request.GET.get('cod')

   if cod_ciudadano is not None:
      ciudadano = CiudadanoModel.objects.get(pk=cod_ciudadano)
      serializer = CiudadanoSerializer(ciudadano)
      return JsonResponse(serializer.data)
   else:
     return JsonResponse({"message": "No se ha encontrado el ciudadano."})
