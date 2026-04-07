from django.contrib import admin
from .models import Cliente, Producto, Estado

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nif', 'nombre', 'email')
    search_fields = ('nif', 'nombre', 'email')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku', 'nombre', 'precio', 'stock')
    search_fields = ('sku', 'nombre')

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
