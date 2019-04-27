from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import PedidoListView, DespachoListView, PedidoListPDF, PedidoCreateView, UpdatePedidoView
from django.conf.urls import url

urlpatterns = [
    path('list/', login_required(PedidoListView.as_view()), name='Plist'),
    path('despacho/', login_required(DespachoListView.as_view()), name='despacho'),
    path('pdf/', login_required(PedidoListPDF.as_view()), name='pdflist'),
    path('nuevo/', login_required(PedidoCreateView.as_view()), name='crear_pedido'),
    # path('detalle/items/<int:pk>', login_required(UpdatePedidoView.as_view()), name='despacho_items'),
    # path('despacho/<int:pk>', login_required(DespachoView.as_view()), name='detalle'),
]
