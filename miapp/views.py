from django.shortcuts import render
from rest_framework.views import APIView  
from django.http import JsonResponse  
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent

import os
import json


from miapp.models import CiudadanoModel
from miapp.serializers import CiudadanoSerializer

# Constantes
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PGDATABASE = os.environ.get('PGDATABASE')
PGUSER =  os.environ.get('PGUSER')
PGPASSWORD = os.environ.get('PGPASSWORD')
PGHOST = os.environ.get('PGHOST')
PGPORT = os.environ.get('PGPORT')  

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
   
   

def query_to_sql(human_query: str):   
   db = get_database()
   llm = ChatOpenAI(model="gpt-4o-mini")
   toolkit = SQLDatabaseToolkit(db=db, llm=llm)
   
   prompt_template =  ChatPromptTemplate.from_messages([
      ("system", '''Usted es un agente diseñado para interactuar con una base de datos SQL.
   Dada una pregunta de entrada, crea una consulta {dialect} sintácticamente correcta para ejecutarla, luego mira los resultados de la consulta y devuelve la respuesta.
   A menos que el usuario especifique un número concreto de ejemplos que desea obtener, limite siempre su consulta a un máximo de {top_k} resultados.
   Puede ordenar los resultados por una columna relevante para obtener los ejemplos más interesantes de la base de datos.
   Nunca pregunte por todas las columnas de una tabla específica, sólo pregunte por las columnas relevantes dada la pregunta.
   Tiene acceso a herramientas para interactuar con la base de datos.
   Utilice únicamente las herramientas que se indican a continuación. Utilice únicamente la información que le proporcionen las siguientes herramientas para elaborar su respuesta final.
   DEBE comprobar su consulta antes de ejecutarla. Si obtiene un error al ejecutar una consulta, reescríbala e inténtelo de nuevo.
   NO realice ninguna sentencia DML (INSERT, UPDATE, DELETE, DROP, etc.) en la base de datos.
   Para empezar, SIEMPRE debes mirar las tablas de la base de datos para ver qué puedes consultar.
   No se salte este paso.
   A continuación, debe consultar el esquema de las tablas más relevantes'''),
   ])
   
   system_message = prompt_template.format(dialect="PostgreSQL", top_k=5)
   agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message
   )

   events = agent_executor.stream(
      {"messages": [("user", human_query)]},
      stream_mode="values",
   )
   response = ""
   for event in events:
      event["messages"][-1].pretty_print()
      response = event["messages"][-1].content

   return response

def get_database():
   uri = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
   db = SQLDatabase.from_uri(uri)
   return db
   
class QueryView(APIView):
  def post(self, request, format=None):
    try:
      human_query = request.data.get('query')
      response = query_to_sql(human_query)
      return JsonResponse({"message": response})
    except Exception as e:
      return JsonResponse({"message": str(e)})