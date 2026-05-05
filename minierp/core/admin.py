from django.contrib import admin
from .models import Cliente, Producto, Estado

@admin.register(Cliente) #Registra el modelo Cliente en el panel de admin
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nif', 'nombre', 'email') #Columnas que se veran en la tabla del admin
    search_fields = ('nif', 'nombre', 'email')#Campos sobre los que se puede buscar

@admin.register(Producto) #Registra el modelo Producto en el panel de admin
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku', 'nombre', 'precio', 'stock')
    search_fields = ('sku', 'nombre')

@admin.register(Estado) #Registra el modelo Estado para pedidos
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
