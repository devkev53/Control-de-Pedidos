from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['tipo', 'nombre', 'apellido', 'direccion', 'telefono', 'nit', 'email']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': "form-control mb-3",
                }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nombre del Cliente'}),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Apellidos'}),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ingrese la direccion'}),
            'telefono': forms.NumberInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Telefono'}),
            'nit': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'NIT', 'value': 'C/F'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Correo Elelectronico'}),
        }
        labels = {
            'title': '', 'order': '',
        }
