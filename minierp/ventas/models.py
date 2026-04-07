from django.db import models
from core.models import Cliente, Producto, Estado
from decimal import Decimal

class Pedido(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
	fecha_creacion = models.DateTimeField (auto_now_add=True)
	estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
	#Nuevos
	iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('21.00'))
	total_base = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

	def __str__(self):
		return f"Pedido {self.id} - {self.cliente}"
	
	def calcular_totales(self):
		base = sum((linea.total_price for linea in self.lineas.all()), Decimal('0.00'))
		self.total_base = base.quantize(Decimal('0.01'))
		self.total_iva = (self.total_base * (self.iva_porcentaje / Decimal('100'))).quantize(Decimal('0.01'))
		self.total_pedido = (self.total_base + self.total_iva).quantize(Decimal('0.01'))

		Pedido.objects.filter(pk=self.pk).update(
			total_base=self.total_base,
			total_iva=self.total_iva,
			total_pedido=self.total_pedido,
		)

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
	
	@property
	def total_price(self):
		return (self.precio_unitario * self.cantidad).quantize(Decimal('0.01'))
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.pedido.calcular_totales()

	def delete(self, *args, **kwargs):
		pedido = self.pedido
		super().delete(*args, **kwargs)
		pedido.calcular_totales()