from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

TIPO_CLIENTE_CHOICES = (
    ('Normal', "Normal"),
    ('Especial', "Especial"),
    ('Mayorista', "Mayorista"),
)


def numeroTelefono(value):  # Funcion no permite menos de 7 #
    if not len(value) > 7:  # Si el largo es menor de 7
        raise ValidationError(  # Muesra un mensaje de error
            'Ingrese un numero de Telefono valido')


class Cliente(models.Model):
    nombre = models.CharField('Nombres', max_length=75)
    apellido = models.CharField('Apellidos', max_length=75)
    direccion = models.CharField('Direccion', max_length=125, default='Ciudad')
    email = models.EmailField('Correo', blank=True)
    telefono = models.CharField(
        'Telefono',
        validators=[RegexValidator(  # Clases para hacer validaciones
            regex=r'^[0-9]*$',  # cadenas permitidas
            message=('Ingrese solamente numeros'),  # Mensaje de error
        ), numeroTelefono], max_length=8, blank=True)  # Caracteres maximos
    nit = models.CharField(
        'No. de NIT',
        validators=[RegexValidator(  # Clases para hacer validaciones
            regex=r'^[0-9 C,F,/,c,f,]*$',  # cadenas permitidas
            message=('Ingrese un NIT Valido'),  # Mensaje de error
        )], max_length=9, default='C/F')  # Caracteres maximos
    tipo = models.CharField(
        'Tipo de Cliente', choices=TIPO_CLIENTE_CHOICES, default='Normal', max_length=15)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)

    '''  Sobrescribimos el metodo save para poder crear una cuenta
    por cada cliente que registremos  '''
    def save(self):
        super(Cliente, self).save()
        cliente = Cliente.objects.filter(id=self.id).get()
        cliente = Cliente.objects.filter(id=self.id).get()
        Cuenta.objects.create(cliente=cliente, saldo=0)
        # saldo = Cuenta.objects.filter(cliente_id=self.id)
        # print(saldo.saldo)
        return cliente


class Cuenta(models.Model):
    cliente = models.OneToOneField(
        Cliente, verbose_name='Cliente', on_delete=models.CASCADE)
    saldo = models.FloatField('saldo', editable=False)

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return '%s El saldo de la cuent es %s' % (
            self.cliente, self.saldo)
