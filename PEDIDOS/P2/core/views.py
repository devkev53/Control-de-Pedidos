from django.shortcuts import render
from django.views.generic import TemplateView
from easy_pdf.views import PDFTemplateView
from orden.models import Pedido, Item
from cliente.models import Cliente
from producto.models import Producto
import datetime



class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {
                'title': 'Mi Super Web Playground 2'})
        pass


#  Vista para mostar el pdf con el lisado de pedidos
class MorososListPDF(PDFTemplateView):
    model = Pedido
    template_name = "reportes/morosos_pdf.html"

    def get_context_data(self, **kwargs):
        cliente = Cliente.objects.all()
        pedido = Pedido.objects.all()
        return super(MorososListPDF, self).get_context_data(
            pagesize='Legal landscape',
            title="Ficha",
            cliente=cliente,
            pedido=pedido,
            **kwargs
            )


#  Vista para mostar el pdf con el lisado de Productos a entregar
#  Mostarara solo las entregas del dia segun el sistema.
class EntregaProductosListPDF(PDFTemplateView):
    model = Pedido
    template_name = "reportes/entregas.html"

    def get_context_data(self, **kwargs):
        item = Item.objects.all()
        pedido = Pedido.objects.all()
        producto = Producto.objects.all()
        today = datetime.date.today

        return super(EntregaProductosListPDF, self).get_context_data(
            pagesize='Legal landscape',
            title="Ficha",
            item=item,
            pedido=pedido,
            producto=producto,
            today=today,
            **kwargs
            )
