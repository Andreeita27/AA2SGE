from django.contrib import admin
from .models import Pedido, LineaPedido

class LineaPedidoInline(admin.TabularInline):
	model = LineaPedido
	extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	inlines = [LineaPedidoInline]
	list_display = ('id', 'cliente', 'fecha_creacion', 'estado')
