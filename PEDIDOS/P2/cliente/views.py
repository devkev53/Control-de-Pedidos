from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Cliente
from .forms import ClienteForm

# Create your views here.


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('Ccreate')

    def get_success_url(self):
        return reverse_lazy('Clist')+'?Cliente/ok'


class ClienteListView(ListView):
    model = Cliente
    template_name = 'profiles/Cliente_list.html'
    paginate_by = 10


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('Clist')+'?Update/ok'
