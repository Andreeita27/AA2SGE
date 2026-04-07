from django.shortcuts import render
from rest_framework.generics import ListAPIView
from core.models import Producto
from .serializers import ProductoSerializer

#Crea el endopoint qe devuelve el listado de productos en JSON usando DRf
class ProductoListAPIView(ListAPIView):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
