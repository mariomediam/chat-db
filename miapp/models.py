from django.db import models

# Modelo Ciudadano
class CiudadanoModel(models.Model):
    ciudadano_cod = models.CharField(max_length=11, primary_key=True, help_text='Código único de identificación del ciudadano.')
    ciudadano_nombre = models.CharField(max_length=100, help_text='Nombre completo del ciudadano.')

    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"
        db_table = 'ciudadano'
        # Descripción de la tabla (no es nativo de Django, pero ayuda a documentar)
        app_label = "Almacena los datos de los ciudadanos."

    def __str__(self):
        return self.ciudadano_nombre