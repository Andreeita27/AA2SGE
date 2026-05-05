from django.shortcuts import render
from rest_framework.generics import ListAPIView #Vista generica de drf para listar datos (GET)
from core.models import Producto #Modelo que expone la api
from .serializers import ProductoSerializer #Serielizer que convierte los datos a json

#Crea el endopoint qe devuelve el listado de productos en JSON usando DRf
class ProductoListAPIView(ListAPIView):
    queryset = Producto.objects.all().order_by('id') #consulta la bbdd: obtiene todos los productos ordenados por id
    serializer_class = ProductoSerializer #serielizer que se utiliza

    def get_serializer_context(self): #Sobrescribe este metodo para pasar datos extra al serializer
        context = super().get_serializer_context() #Obtiene el contexto por defecto
        context['request'] = self.request #Necesario que el serializer sepa si el usuario esta autenticado
        return context #devuelve el contexto completo
