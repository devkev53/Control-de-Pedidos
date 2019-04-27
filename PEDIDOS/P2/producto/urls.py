from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ProductoListView, ProductoCreateView
from .views import ProductoDetailView, ProductoDeleteView, ProductoUpdateView

urlpatterns = [
    path('listado/', ProductoListView.as_view(), name='list'),
    path('create/', login_required(ProductoCreateView.as_view()), name='create'),
    path(
        '<int:pk>/',
        ProductoDetailView.as_view(), name='producto'),
    path('delete/<int:pk>', ProductoDeleteView.as_view(), name='delete'),
    path('update/<int:pk>', ProductoUpdateView.as_view(), name='update'),
]