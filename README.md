# API de Consultas en Lenguaje Natural a Base de Datos en Supabase

Esta API permite realizar consultas en lenguaje natural a una base de datos alojada en **Supabase** utilizando OpenAI, Django y LangChain. La API traduce preguntas complejas en lenguaje humano a consultas SQL, devolviendo los resultados directamente desde la base de datos.

## Características

- **Consultas en lenguaje natural**: Realiza preguntas sobre la base de datos sin necesidad de escribir SQL.
- **Respuestas precisas**: El sistema genera consultas SQL basadas en la comprensión de la pregunta.
- **Tecnología avanzada**: Implementada con OpenAI para el procesamiento del lenguaje natural y LangChain para gestionar las interacciones con la base de datos.

## Tecnologías Utilizadas

- **Django**: Framework utilizado para construir la API.
- **LangChain**: Herramienta de procesamiento avanzado de lenguaje natural y manipulación de consultas.
- **OpenAI**: Provee la inteligencia artificial para interpretar preguntas en lenguaje natural.
- **Supabase**: Plataforma de base de datos que usa PostgreSQL, en la que se realizan las consultas.

## Cómo Funciona

1. **Enviar una pregunta**: El usuario puede enviar una consulta en lenguaje natural (por ejemplo: "¿Cuántos usuarios se registraron el mes pasado?").
2. **Traducción de la pregunta a SQL**: La API convierte la consulta en una instrucción SQL válida.
3. **Consulta a Supabase**: El sistema ejecuta la consulta en la base de datos Supabase.
4. **Respuesta JSON**: Se devuelve el resultado de la consulta en formato texto

## Ejemplo de Consulta y Respuesta

- **Pregunta**: "¿quien presento el expediente 5 del año 2024?"
- **Respuesta en JSON**:
    ```json
    {
    "message": "El expediente 5 del año 2024 fue presentado por Aissa Alexandra Huacchillo Crisanto."
    }
    ```

## Deploy con docker compose

Antes de empezar, [instala Compose](https://docs.docker.com/compose/install/).

```
$ docker compose up -d
```


Después de que se inicie la aplicación ejecute la API `http://localhost:8000/query/` tal como se indica en el video anterior:


