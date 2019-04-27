from django.db import models

# Create your models here.


class TipoPago(models.Model):
    descripcion = models.CharField('Descripcion', max_length=10)

    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pagos"

    def __str__(self):
        return '%s' % (self.descripcion)
