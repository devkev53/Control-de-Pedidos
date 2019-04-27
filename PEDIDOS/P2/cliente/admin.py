from django.contrib import admin
from .models import Cliente, Cuenta

# Register your models here.


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'cuenta']


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Cuenta)
