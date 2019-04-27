from django.db import models
from cliente.models import Cliente, Cuenta
from producto.models import Producto
import random
# Importamos para realicar un signal
from django.db.models.signals import post_save
from django.dispatch import receiver

# Importamos la exepcion para mostrar el mensage de erro de validacion
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from core.models import TipoPago
import datetime

# Create your models here.

TIPOPAGO_CHOICES = (
    ('1', "Efectivo"),
    ('2', "Deposito"),
    ('3', "Cheque"),
    ('4', 'Otro')
)

PAGO_CHOICES = (
    ('1', "Sin Pago"),
    ('2', "Parcial"),
    ('3', "Pendiente")
)


def morosos(cliente):
    print()


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente, verbose_name='Cliente', on_delete=models.CASCADE)
    total = models.FloatField('Total', editable=False, default=0)
    abono = models.FloatField('Abono', default=0)
    pago = models.CharField(
        'Pago', choices=PAGO_CHOICES, max_length=10, blank=True)
    tipo_pago = models.ManyToManyField(
        TipoPago, verbose_name='Tipo de Pago', default=0)
    create = models.DateTimeField(auto_now_add=True, editable=False)
    finalizado = models.BooleanField('Finalizado', default=False)
    entrega = models.DateField('Fecha de Entrega', default=datetime.date.today)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return '%s' % (self.cliente)

#  Este metodo permite recoger un listado de campos Many to Many
    def recoge_tipo_pago(self):
        return ", \n".join([t.descripcion for t in self.tipo_pago.all()])

#  Funcion para mostar el link de descarga de cada pedido
    def listado(self):
        return mark_safe(u'<a href="/BoletaPedido/?id=%s" target="_blank">Descargar</a>' % self.id)
    listado.short_description = 'Boleta'

#  Funcion que realiza la suma total de los items del detalle de pedido
    def recoge_total(self):
        items = Item.objects.filter(Pedido__id=self.id)
        total = 0
        for items in items:
            p = items.producto.precio
            c = items.cantidad
            sub = p*c
            total = total+sub
        if self.cliente.tipo == 'Normal':
            total = total
        if self.cliente.tipo == 'Especial':
            descuento = (total*(10/100))
            total = total - descuento
        if self.cliente.tipo == 'Mayorista':
            descuento = (total*(15/100))
            total = total - descuento
        self.total = float(total)
        super(Pedido, self).save()
        return total
    recoge_total.short_description = ('Consumo')

#  Funcion que verifica si los items fueron despachados
    def estado(self):
        items = Item.objects.filter(Pedido__id=self.id)
        tproductos = 0
        estado = 'Pendiente'
        cont = 0
        for items in items:
            tproductos += 1
            if items.despacho is True:
                cont += 1
        if tproductos == cont:
            estado = 'Despachado'
            self.finalizado = True
        else:
            estado = 'Pendiente'
            self.finalizado = False
        super(Pedido, self).save()
        return estado
    estado.short_description = ('Finalizado')

#  Muestra el tipo de pago realizado
    def pago(self):
        if self.abono > 0.0:
            if self.abono == self.recoge_total():
                self.pago = 'Total'
            else:
                self.pago = 'Parcial'
        else:
            self.pago = 'N/A'
        return self.pago

#  Funcion que muestra el saldo pendiente de cancelar en el pedido
    def saldo_pendiente(self):
        total = self.recoge_total()
        saldo = total-self.abono
        return float(saldo)

    def clean(self):
        if self.entrega < datetime.date.today():
            raise ValidationError("Debe seleccionar una fecha valida..!")
        return self.entrega

    def suma_saldos(self):
        saldo = self.saldo_pendiente()
        print('Muestra Suma de saldos desde la funcion: ', saldo)
        nuevo = (saldo-(saldo*2))
        cuenta = Cuenta.objects.filter(cliente__id=self.cliente.id)
        anterior = Cuenta.objects.filter(cliente__id=self.cliente.id).get()
        print(anterior.saldo)
        if anterior.saldo == 0:
            print('el saldo era igual a: 0')
            return cuenta.update(saldo=nuevo)
            print('El nuevo saldo es de: ', nuevo)
        else:
            print('el saldo anterior es de: ', anterior.saldo)
            new_saldo = (anterior.saldo+nuevo)
            return cuenta.update(saldo=new_saldo)
            print('El nuevo saldo es de: ', new_saldo)

    def descuento(self):
        items = Item.objects.filter(Pedido__id=self.id)
        total = 0
        descuento=0
        for items in items:
            p = items.producto.precio
            c = items.cantidad
            sub = p*c
            total = total+sub
        if self.cliente.tipo == 'Normal':
            total = total
        if self.cliente.tipo == 'Especial':
            descuento = (total*(10/100))
            total = total - descuento
        if self.cliente.tipo == 'Mayorista':
            descuento = (total*(15/100))
            total = total - descuento
        return descuento

    def save(self):
        self.total = self.recoge_total()
        super(Pedido, self).save()


class Item(models.Model):
    producto = models.ForeignKey(
        Producto, verbose_name='Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField('Cantidad', default=0)
    Pedido = models.ForeignKey(
        Pedido, verbose_name='Pedido', on_delete=models.CASCADE)
    despacho = models.BooleanField('Despachado', default=False, blank=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return '%s' % (self.producto)

    def subtotal(self):
        p = self.producto.precio
        c = self.cantidad
        sub = p*c
        return sub

'''
# Funcion con Signal para detectar la creacion del Item del Pedido realizar la suma de saldos
@receiver(post_save, sender=Pedido)
def post_save_pedido(sender, instance, **kwargs):
    # Verifico que se crea un Pedido
    pedido = instance
    if kwargs['created']:
        # hago las acciones que necesito
        nuevo = Pedido.objects.filter(id=pedido.id)
        nuevo.update()
        pedido = nuevo.get()
        print('Se a Creado un Pedido')
        print(pedido.total)
        nuevo.update()
        print(pedido.recoge_total())
        print(pedido.create)'''


#  Funcion Signal que sumara los pedidos a la cuenta del cliente
#  Suma el subtotal de item en detalle y los resta de la cuenta del cliente
#  haciendo asi que su cuenta se muestre en mora
@receiver(post_save, sender=Item)
def post_save_item(sender, instance, **kwargs):
     # Verifico que se crea un Pedido
    item = instance
    total = 0
    saldo = 0
    producto = Producto.objects.filter(id=item.producto.id).get()
    pedido = Pedido.objects.filter(id=item.Pedido.id).get()
    cliente = Cliente.objects.filter(id=pedido.cliente.id).get()
    cuenta = Cuenta.objects.filter(cliente__id=cliente.id)
    if kwargs['created']:
        total = item.cantidad*producto.precio
        saldo = cliente.cuenta.saldo
        suma = saldo - total
        cuenta.update(saldo=suma)


# Funcion con Signal para detectar la creacion del Item del Pedido realizar la suma de saldos
# suma el abono realizado en el pedido a la cuenta del cliente reflejando en esta el monto abonado
@receiver(post_save, sender=Pedido)
def post_save_pedido(sender, instance, **kwargs):
    # Verifico que se crea un Pedido
    pedido = Pedido.objects.filter(id=instance.id).get()
    cliente = Cliente.objects.filter(id=instance.cliente.id).get()
    cuenta = Cuenta.objects.filter(cliente__id=cliente.id)
    abono = pedido.abono
    saldo = 0
    if kwargs['created']:
        print('Se esta creando un Pedido el abono es de: ', abono)
        saldo = cliente.cuenta.saldo
        print('Saldo antes del update: ', cliente.cuenta.saldo)
        suma = saldo+abono
        cuenta.update(saldo=suma)
        print('Saldo despues del update: ', cliente.cuenta.saldo)
