"""P2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from orden.views import BoletaPedido
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # path de la app core
    path('', include('core.urls')),
    # path de django contrib para la autenticacion
    path('accounts/', include('django.contrib.auth.urls')),
    # path de registration
    path('accounts/', include('registration.urls')),
    # path de Producto
    path('producto/', include('producto.urls')),
    # path de Cliente
    path('cliente/', include('cliente.urls')),
    # path de Pedido
    path('orden/', include('orden.urls')),
    # URL detalle de Pedido PDF
    url(r"^BoletaPedido/(?P<id>)", BoletaPedido.as_view()),
]

# Truco para poder ver ficheros multimedia con el DEBUG=TRUE
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom titles para el admin
admin.site.site_header = 'Control de Pedidos'
#  admin.site.index_title = 'No se que poner XD'
admin.site.site_title = 'Pedidos'
