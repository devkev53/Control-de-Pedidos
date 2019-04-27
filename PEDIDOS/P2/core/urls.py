from django.urls import path
from .views import HomePageView, MorososListPDF, EntregaProductosListPDF

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('morosos/', MorososListPDF.as_view(), name="moras"),
    path('entregas/', EntregaProductosListPDF.as_view(), name="entregas"),
]
