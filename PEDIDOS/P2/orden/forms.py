from django import forms
from .models import Pedido, Item
from django.forms.models import inlineformset_factory
from cliente.models import Cuenta
import datetime


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={
                'class': "form-control mb-3 mt-3 col-4",
                }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control mb-3 mt-3 col-4',
                }),
        }
        labels = {
            'title': '', 'order': '',
        }


class ItemDespachoForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['producto', 'cantidad', 'despacho']
        widgets = {
            'producto': forms.Select(attrs={
                'class': "form-control mb-3 mt-3 col-4",
                'editable': False, 'readonly': True,
                }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control mb-3 mt-3 col-4',
                'editable': False, 'readonly': True,
                }),
            'despacho': forms.CheckboxInput(attrs={
                'class': 'form-control mb-3 mt-3 col-4',
                'required': False, 'default': False,
                }),
        }
        labels = {
            'title': '', 'order': '',
        }

class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'abono', 'tipo_pago']
        widgets = {
            'id': forms.TextInput(attrs={
                'class': "form-control mb-3",
                }),
            'abono': forms.NumberInput(attrs={
                'class': "form-control mb-3",
                'placeholder': 'Cantidad de Abono'
                }),
            'cliente': forms.Select(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Cliente'}),
            'pago': forms.Select(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Pago'}),
            'tipo_pago': forms.SelectMultiple(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Tipo de Pago'}),
        }
        labels = {
            'title': '', 'order': '',
        }


#  Formularios nuevos 22-04-19
# import para crear el fromset inline
from django.forms.models import inlineformset_factory


#  Formulario de Pedido
class NuevoPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'abono', 'tipo_pago', 'entrega')
        widgets = {
            'id': forms.TextInput(attrs={
                'class': "form-control mb-3",
                }),
            'abono': forms.NumberInput(attrs={
                'class': "form-control mb-3",
                'placeholder': 'Cantidad de Abono'
                }),
            'cliente': forms.Select(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Cliente'}),
            'pago': forms.Select(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Pago'}),
            'tipo_pago': forms.SelectMultiple(attrs={
                'class': 'form-control mb-3'}),
            'entrega': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control mb-3'}),
        }
        labels = {
            'title': '', 'order': '',
        }

        def clean_fecha(self):
            entrega = self.cleaned_data.get('entrega')

            if entrega < datetime.date.today():
                raise forms.ValidationError('Ingrese una fecha valida..!')
            return entrega

        def clean_entrega(self):
            fecha = datetime.date.today
            self.entrega.value = fecha
            return fecha


#  Formulario de Detalle
class DetalleForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('producto', 'cantidad')
        widgets = {
            'producto': forms.Select(attrs={
                'class': "form-control mb-3",
                }),
            'cantidad': forms.NumberInput(attrs={
                'class': "form-control mb-3",
                'placeholder': 'Cantidad de Abono'
                }),
        }

DetallePedidoFormSet = inlineformset_factory(Pedido, Item, DetalleForm, extra=1)

''' Para la edicion de los pedidos y marcado de los despachos'''
#  Formulario de Pedido
class UpdatePedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'abono', 'tipo_pago', 'entrega')
        widgets = {
            'id': forms.TextInput(attrs={
                'class': "form-control mb-3", 'readonly': True
                }),
            'abono': forms.NumberInput(attrs={
                'class': "form-control mb-3",
                'placeholder': 'Cantidad de Abono',
                'readonly': True
                }),
            'cliente': forms.Select(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Cliente',
                'readonly': True, 'editable': False}),
            'pago': forms.Select(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Pago',
                'readonly': True}),
            'tipo_pago': forms.SelectMultiple(attrs={
                'class': 'form-control mb-3',
                'readonly': True}),
            'entrega': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control mb-3',
                'readonly': True}),
        }
        labels = {
            'title': '', 'order': '',
        }

