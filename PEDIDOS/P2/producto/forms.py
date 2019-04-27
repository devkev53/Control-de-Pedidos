from django import forms
from .models import Producto
from django.contrib.admin.widgets import FilteredSelectMultiple


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['categoria', 'nombre', 'descrip', 'img', 'precio']
        widgets = {
            'categoria': forms.SelectMultiple(attrs={
                'class': "form-control mb-3",
                }),
            'img': forms.FileInput(attrs={
                'type': 'file', 'class': 'custom-file-input',
                'id': 'inputGroupFile03',
                'aria-describedby': 'inputGroupFileAddon03'
                }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nombre del Articulo'}),
            'descrip': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 4, 'placeholder': 'Descripcion del Producto'}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Precio'}),
        }
        labels = {
            'title': '', 'order': '',
        }
