from django.db import models
from core.models import Cliente, Producto, Estado

class Pedido(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
	fecha_creacion = models.DateTimeField (auto_now_add=True)
	estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

	def __str__(self):
		return f"Pedido {self.id} - {self.cliente}"

class LineaPedido(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
	producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
	cantidad = models.IntegerField()
	precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al momento de la venta")

	class Meta:
	# Crea la regla de que la cantidad debe ser mayor que 0 en la bbdd.
		constraints = [
			models.CheckConstraint(
				check=models.Q(cantidad__gt=0),
				name='cantidad_positiva_check'
			)
		]

	def __str__(self):
		return f"{self.cantidad}x {self.producto.nombre}"