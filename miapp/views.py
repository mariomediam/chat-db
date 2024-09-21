from django.shortcuts import render
from rest_framework.views import APIView  
from django.http import JsonResponse  
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain

import os
import json


from miapp.models import CiudadanoModel
from miapp.serializers import CiudadanoSerializer

# Constantes
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

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
   respuesta = human_query_to_sql("Que ciudadano tiene el código 0010389?")
   print(respuesta)

   if cod_ciudadano is not None:
      ciudadano = CiudadanoModel.objects.get(pk=cod_ciudadano)
      serializer = CiudadanoSerializer(ciudadano)
      return JsonResponse(serializer.data)
   else:
     return JsonResponse({"message": "No se ha encontrado el ciudadano."})
   
def get_schema():
  schema = '''
   table
   public.ciudadano (
      ciudadano_cod character(11) not null,
      ciudadano_nombre character varying(100) null,
      constraint ciudadano_pkey primary key (ciudadano_cod)
   ) tablespace pg_default;


   table
   public.tramite (
      tramite_cod character(13) not null,
      tramite_nombre character varying(100) null,
      constraint tramite_pkey primary key (tramite_cod)
   ) tablespace pg_default;


   table
   public.expediente (
      exped_nro character(8) not null,
      exped_anio character(4) not null,
      exped_fecing timestamp without time zone null,
      exped_observ character varying(700) null,
      ciudadano_cod character(11) null,
      tramite_cod character(13) null,
      exped_finalizado boolean null,
      constraint expediente_pkey primary key (exped_nro, exped_anio),
      constraint expediente_ciudadano_cod_fkey foreign key (ciudadano_cod) references ciudadano (ciudadano_cod),
      constraint expediente_tramite_cod_fkey foreign key (tramite_cod) references tramite (tramite_cod)
   ) tablespace pg_default;
   '''   
  return schema

class ResponseQueryFormat(BaseModel):
    """Retorna los datos de la consulta en formato JSON."""
    sql_query: str = Field(..., description="Consulta en SQL que recupera la información solicitada.")
    original_query: str = Field(..., description="Consulta original en lenguaje humano.")

# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(..., description="question to set up a joke")
    punchline: str = Field(..., description="answer to resolve the joke")

    

def human_query_to_sql(human_query: str):
   database_schema = get_schema()
   PROMPT_SYSTEM_TEMPLATE = ''' Dado el siguiente esquema, escriba una consulta SQL que recupere la información solicitada. 
    Devuelve la consulta SQL dentro de una estructura JSON con la clave "sql_query".

   <example>{{
        "sql_query": "SELECT * FROM expediente WHERE exped_anio ='2024';"
        "original_query": "Que expedientes se han registrado en el año 2024?"
    }}
    </example>
    <schema>
    {context}
    </schema>
   '''

   PROMT_USER_TEMPLATE = '''Escribe una consulta SQL que recupere la información solicitada.
   {context}
   '''
   llm = ChatOpenAI(model="gpt-4o-mini")
   model = ChatOpenAI(temperature=0)
   prompt = ChatPromptTemplate.from_messages(
      [("system", PROMPT_SYSTEM_TEMPLATE),
       ("user", PROMT_USER_TEMPLATE)],
   )
   # parser = JsonOutputParser(pydantic_object=ResponseQueryFormat)
   # chain = create_stuff_documents_chain(llm, prompt, output_parser=parser)

   # # Invoke chain
   # And a query intented to prompt a language model to populate the data structure.
   structured_llm = llm.with_structured_output(ResponseQueryFormat)
   # response = structured_llm.invoke("Tell me a joke about cats")
   return response


class Joke(BaseModel):
    '''Joke to tell user.'''

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    



