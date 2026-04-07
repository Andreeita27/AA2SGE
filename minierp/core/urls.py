from django.urls import path
from .views import HomeView, ProductoCreateView, ClienteCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('productos/add/', ProductoCreateView.as_view(), name='producto_add'),
    path('clientes/add/', ClienteCreateView.as_view(), name='cliente_add'),
]