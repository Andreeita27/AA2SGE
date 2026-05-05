from rest_framework import serializers #importa sistema de serializacion de drf
from core.models import Producto #importa modelo producto

class ProductoSerializer(serializers.ModelSerializer): #serializer basado en el modelo producto
    #Convierte objetos de djano a json automaticamente
    stock = serializers.SerializerMethodField() #Define el stock cmo un campo calculado que no se devuelve automaticamente

    class Meta:
        model = Producto #modelo que se serializa
        fields = ['id', 'sku', 'nombre', 'precio', 'stock'] #campos del json

    def get_stock(self, obj): #metodo que se ejecuta para calcular el campo stock
        request = self.context.get('request') #Obtiene la request desde el contexto (pasa desde la vista)

        #Devuelve stock si el usuario esta autenticado
        if request and request.user.is_authenticated:
            return obj.stock
        
        return None #Si no esta autenticado -> oculta stock