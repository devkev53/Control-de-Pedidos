from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Producto, Categoria
from .forms import ProductoForm
# Create your views here.


class ProductoListView(ListView):
    model = Producto
    template_name = 'profiles/producto_list.html'
    paginate_by = 8


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('list')

    def get_context_data(self, *args, **kwargs):
        fc = ProductoForm
        cat = Categoria.objects.all()

        return {'form': fc, 'cat': cat}


class ProductoDetailView(DetailView):
    model = Producto


@method_decorator(staff_member_required, name='dispatch')
class ProductoDeleteView(DeleteView):
    model = Producto
    success_url = reverse_lazy('list')


@method_decorator(staff_member_required, name='dispatch')
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('list')+'?Update/ok'
