from django.contrib import admin
from .models import Pedido, LineaPedido #importo modelos relacionados con ventas

class LineaPedidoInline(admin.TabularInline): #permite editar lineas de pedido dentro del pedido
	model = LineaPedido #Modelo hijo (las lineas)
	extra = 1 #filas vacias que aparecen por defecto para añadir lineas nuevas facilmente

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	inlines = [LineaPedidoInline] #Conecta las lineas con el pedido y permite crearlas y editarlas
	list_display = ('id', 'cliente', 'fecha_creacion', 'estado', 'total_base', 'total_iva', 'total_pedido',)
	#Campos visibles, incluye los totales calculados
