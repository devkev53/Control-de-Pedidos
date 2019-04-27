from django.db import models


# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField('Nombre', max_length=75)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class SubCategoria(models.Model):
    nombre = models.CharField('Nombre', max_length=75)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Sub-Categoria"
        verbose_name_plural = "Sub-Categorias"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField('Nombre', max_length=75)
    descrip = models.TextField('Descripcion')
    img = models.ImageField(upload_to='prdoucto/', null=True, blank=True)
    precio = models.FloatField('Precio')
    categoria = models.ManyToManyField(
        SubCategoria, verbose_name='Categorias', blank=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return '%s Q %s' % (self.nombre, self.precio)
