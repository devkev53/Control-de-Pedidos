from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ClienteCreateView, ClienteListView, ClienteUpdateView

urlpatterns = [
    path('create/', login_required(ClienteCreateView.as_view()), name='Ccreate'),
    path('listado/', login_required(ClienteListView.as_view()), name='Clist'),
    path('update/<int:pk>', ClienteUpdateView.as_view(), name='Cupdate'),
]
