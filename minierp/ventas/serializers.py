from rest_framework import serializers
from core.models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'sku', 'nombre', 'precio', 'stock']

    def get_stock(self, obj):
        request = self.context.get('request')

        #Devuelve stock si el usuario esta autenticado
        if request and request.user.is_authenticated:
            return obj.stock
        
        return None