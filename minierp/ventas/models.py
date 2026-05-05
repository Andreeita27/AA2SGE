from django.db import models #orm de Django para crear modelos/tablas
from core.models import Cliente, Producto, Estado #modelos de la app core
from decimal import Decimal

class Pedido(models.Model): #Modelo pedido
	cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT) #restrict impide borrar un cliente si tiene pedidos asociados
	fecha_creacion = models.DateTimeField (auto_now_add=True) #Fecha automaticade creacion
	estado = models.ForeignKey(Estado, on_delete=models.PROTECT) #protect impide borrar un estado si esta siendo usado por pedidos
	#Nuevos
	iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('21.00'))
	total_base = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) #base + iva

	def __str__(self): #Representacion textual del pedido
		return f"Pedido {self.id} - {self.cliente}"
	
	def calcular_totales(self): #logica de negocio, calcula base, iva y total a partir de las lineas de pedido
		base = sum((linea.total_price for linea in self.lineas.all()), Decimal('0.00'))
		#Recorre todas las lineas del pedido, self.lineas.all funciona por related_name =lineas
		#Suma el total de cada linea
		self.total_base = base.quantize(Decimal('0.01')) #Redondea la base a dos decimales
		self.total_iva = (self.total_base * (self.iva_porcentaje / Decimal('100'))).quantize(Decimal('0.01')) #calcula iva
		self.total_pedido = (self.total_base + self.total_iva).quantize(Decimal('0.01')) #total = base + iva

		Pedido.objects.filter(pk=self.pk).update( #actualiza directamente el pedido en la bbdd
			total_base=self.total_base,
			total_iva=self.total_iva,
			total_pedido=self.total_pedido,
		)

class LineaPedido(models.Model): #Modelo linea de pedido
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas') #Relacion con pedido
	#cascade borra las lineas si se borra el pedido
	#related_name='lineas' permite acceder con pedido.lineas.all()
	producto = models.ForeignKey(Producto, on_delete=models.RESTRICT) #restrict impide borrar productos que ya tienen linea de pedido
	cantidad = models.IntegerField()
	precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al momento de la venta")
	#Precio guardado en la linea. Importante porque podría cambiar en el futuro, así mantiene en precio que tenia al momento de la venta

	class Meta:
	# Crea la regla de que la cantidad debe ser mayor que 0 en la bbdd.
		constraints = [
			models.CheckConstraint(
				condition=models.Q(cantidad__gt=0),
				name='cantidad_positiva_check'
			)
		]

	def __str__(self): #Representacion textual d la linea
		return f"{self.cantidad}x {self.producto.nombre}"
	
	@property
	def total_price(self): #Propiedad calculada, no se guarda directamente en la bbdd
		return (self.precio_unitario * self.cantidad).quantize(Decimal('0.01'))
	
	def save(self, *args, **kwargs): #Sobrescribe save para añadir logica automatica
		super().save(*args, **kwargs) #Primero guarda la linea normalmente
		self.pedido.calcular_totales()#Despues recalcula los totales del pedido

	def delete(self, *args, **kwargs):#Sobrescribe delete para recalcular tb al borrar lineas de pedido
		pedido = self.pedido #Guarda la referencia antes de borrar la linea
		super().delete(*args, **kwargs) #Borra
		pedido.calcular_totales() #Recalcula totales