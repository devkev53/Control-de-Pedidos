from django.contrib import admin
from .models import Producto, Categoria, SubCategoria
# Register your models here.


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']
    list_filter = ['categoria']
    search_fields = ('nombre', 'categoria__nombre', 'precio')


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
