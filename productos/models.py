from django.contrib.auth.models import Group, User #importa los modelos Group y user
from django.db import models#importa los metodos necesarios para trabajar con modellos

# Create your models here.


class Local(models.Model):
    id_local = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID Local')
    nombre_local = models.CharField(max_length=50,help_text='Ingrese nombre del local', null=False, blank=False, verbose_name='Nombre Local')
    telefono = models.CharField(max_length=13, null=False, blank=False,help_text='+xxx xxxxxxxx',verbose_name='Teléfono')
    direccion = models.CharField(max_length=200,verbose_name='Direccion')
    encargado = models.CharField(max_length=100, help_text='Ingrese nombre y apellido del encargado',verbose_name='Encargado')
    num_bodegas = models.IntegerField( null=False, blank=False ,verbose_name='Numero de bodegas')
    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')

    class Meta: 
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'
        ordering = ['nombre_local'] 

    def __str__(self):
        return self.nombre_local
    
class Bodega(models.Model):
    id_bodega = models.AutoField(auto_created=True, primary_key=True, serialize=False,verbose_name='ID bodega')
    nombre_bodega = models.CharField(max_length=100,verbose_name='Nombre de bodega')
    TAMAÑOS = (
        ('S', 'Bodega Standar'),
        ('L', 'Bodega Large'),
        ('XL', 'Bodega Extra-Large'),
    )
    tamaño = models.CharField(max_length=4, choices=TAMAÑOS,verbose_name='Tamaño')
    TIPOS = (
        ('SECA', 'Bodega Seca'),
        ('FRÍA', 'Bodega Fría'),
    )
    tipo = models.CharField(max_length=4, choices=TIPOS,verbose_name='ID bodega')
    arrendada = models.BooleanField(null=False, blank=False, default=False, verbose_name='Arrendada')
    fecha_inicio_arriendo = models.DateField(blank=True, null=True,verbose_name='Inicio del ')
    fecha_fin_arriendo = models.DateField(blank=True, null=True,verbose_name='ID bodega')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    local = models.ForeignKey(Local, on_delete=models.CASCADE,verbose_name='Local')

    class Meta: 
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['nombre_bodega'] 


    def __str__(self):
        return self.nombre_bodega


