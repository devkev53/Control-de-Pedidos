from django.contrib import admin
from .models import Pedido, Item

# Register your models here.


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'cliente', 'recoge_tipo_pago', 'create', 'pago',
        'recoge_total', 'saldo_pendiente', 'listado', 'estado', 'entrega', 'descuento']
    inlines = [ItemInline]


class ItemAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'subtotal', 'Pedido']


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Item, ItemAdmin)
