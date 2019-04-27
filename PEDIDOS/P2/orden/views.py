from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
# from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Pedido, Item
from .forms import PedidoForm, ItemForm, ItemDespachoForm
from easy_pdf.views import PDFTemplateView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView
from extra_views import SearchableListMixin, NamedFormsetsMixin, InlineFormSetView
#  Necesitamos la clase cliente para mostarala en el templete de create
from cliente.models import Cliente
import time
# Nuevas importaciones
from .forms import NuevoPedidoForm, UpdatePedidoForm
from django.http import HttpResponseRedirect
#  Importamos el formset inline creado
from .forms import DetallePedidoFormSet, DetalleForm
import datetime

# Create your views here.


#  Creando la vista del pedido con Django Extra-Views
#  usando modelos en linea
class DetalleInline(InlineFormSetFactory):
    model = Item
    form_class = DetalleForm
    factory_kwargs = {'extra': 5, 'max_num': None,
                      'can_order': False, 'can_delete': False}


#  Detalle Despacho Inline
class DetalleDespachoInline(InlineFormSetFactory):
    model = Item
    form_class = ItemDespachoForm
    factory_kwargs = {'extra': 5, 'max_num': None,
                      'can_order': False, 'can_delete': False}


#  Crear un Nuevo Pedido por medio de los templates
class PedidoCreateView(NamedFormsetsMixin, CreateWithInlinesView):
    model = Pedido
    form_class = NuevoPedidoForm
    inlines = [DetalleInline]
    inlines_names = ['detalle']
    template_name = "orden/nuevo_pedido.html"
    success_url = reverse_lazy('Plist')


# Actualizar un Pedido por Medio de los templates
class UpdatePedidoView(NamedFormsetsMixin, UpdateWithInlinesView):
    model = Pedido
    form_class = UpdatePedidoForm
    inlines = [DetalleDespachoInline]
    inlines_names = ['detalle']
    template_name = 'orden/despacho_item.html'

    def get_success_url(self):
        return reverse_lazy('Plist')+'?Update/ok'


#  Vista de despacho de los pedidos
class DespachoView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "orden/despacho_item.html"

    def get_success_url(self):
        return reverse_lazy('despacho')+'?Update/ok'


@method_decorator(staff_member_required, name='dispatch')
class OrdenCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    success_url = reverse_lazy('Plist')


# Vista para mostar la lista de Pedidos
class PedidoListView(SearchableListMixin, ListView):
    search_fields = ['cliente', 'create']
    model = Pedido
    template_name = "orden/pedido_list.html"


# Vista par el despacho
class DespachoListView(SearchableListMixin, ListView):
    search_fields = ['cliente', 'create']
    model = Pedido
    template_name = "orden/despacho.html"
    today = datetime.date.today

    def get_context_data(self, *args, **kwargs):
        pedido = Pedido.objects.all()
        today = datetime.date.today

        return {'pedido': pedido, 'today': today}


#  Vista para mostar el PDF con el lisado de pedidos PDF
class PedidoListPDF(PDFTemplateView):
    model = Pedido
    template_name = "orden/listado_pdf.html"

    def get_context_data(self, **kwargs):
        pedido = Pedido.objects.all()
        return super(PedidoListPDF, self).get_context_data(
            pagesize='Legal landscape',
            title="Ficha",
            pedido=pedido,
            **kwargs
            )


#  Vista para mostrar el detalle del pedido PDF
class BoletaPedido(PDFTemplateView):
    model = Item
    template_name = 'orden/detalle_pedido_pdf.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        pedido = Pedido.objects.get(id=ids)
        items = Item.objects.filter(Pedido__id=pedido.id)

        return super(BoletaPedido, self).get_context_data(
            pagesize='Letter',
            title='Solicitud de Referencia',
            pedido=pedido,
            items=items,
            **kwargs
            )
