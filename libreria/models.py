import requests
from django.db import models
from .services import get_current_datetime  # Importa la función que interactúa con el microservicio

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='Titulo')
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)
    descripcion = models.TextField(verbose_name='Descripcion', null=True)
    direccion = models.TextField(verbose_name='Direccion', null=True)
    publicado = models.BooleanField(default=False, verbose_name='Publicado')  # Nuevo campo para el estado
    fecha_publicacion = models.TextField(null=True, blank=True, verbose_name='Fecha de Publicación')  # Nuevo campo para la fecha y hora

    def __str__(self):
        fila = f"Titulo: {self.titulo} - Descripcion: {self.descripcion} - Direccion: {self.direccion}"
        return fila

    def delete(self, using=None, keep_parent=False):
        # Eliminar la imagen asociada al producto antes de borrarlo
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

    def publicar(self):
        """Marca el producto como publicado y registra la fecha y hora actual
        obtenida desde el microservicio.
        """
        if not self.publicado:  # Solo permite publicar si aún no está publicado
            self.publicado = True
            self.fecha_publicacion = get_current_datetime()  # Obtiene la fecha y hora desde el microservicio
            self.save()
