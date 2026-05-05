from django.shortcuts import render #Permite renderizar templates
from django.urls import reverse_lazy #Sirve para redirigir después de una acción (tras guardar formulario)
from django.views.generic import CreateView, TemplateView #Importa vistas genéricas de Django
from .forms import ClienteForm, ProductoForm #formularios que hemos creado
from .models import Cliente, Producto # Los modelos

class HomeView(TemplateView): #vista simple para mostrar una pag html
    template_name = 'core/home.html' #Indica que template se renderiza

#Vista generica para crear producto
class ProductoCreateView(CreateView):
    model = Producto #Modelo con el que trabaja
    form_class = ProductoForm #Formulario que se va a usar
    template_name = 'core/producto_form.html' #Template que se mostrará
    success_url = reverse_lazy('producto_add') #Redirige despues de guardar
    #Reverse_lazy busca la url por nombre

#Vista alta cliente
class ClienteCreateView(CreateView):
    model = Cliente #Modelo con el que trabaja
    form_class = ClienteForm #formulario que se va a usar
    template_name = 'core/cliente_form.html' #Template que se muestra
    success_url = reverse_lazy('cliente_add') #Redirige despues de guardar