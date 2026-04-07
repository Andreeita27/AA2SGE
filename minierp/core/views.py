from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import ClienteForm, ProductoForm
from .models import Cliente, Producto

class HomeView(TemplateView):
    template_name = 'core/home.html'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/producto_form.html'
    success_url = reverse_lazy('producto_add')

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'core/cliente_form.html'
    success_url = reverse_lazy('cliente_add')