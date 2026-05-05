from django.db import models

class Cliente(models.Model): #Modelo cliente
	nif = models.CharField(max_length=9, unique=True, verbose_name="NIF") #NIF unico
	nombre = models.CharField(max_length=100)
	email = models.EmailField() #EmailField valida que tenga formato email

	def __str__(self): #Define como se muestra un cliente cuando se imprime como texto (admin, desplegables)
		return f"{self.nombre} ({self.nif})"

class Producto(models.Model): #Modelo prodcuto
	sku = models.CharField(max_length=12, unique=True, verbose_name="SKU")
	nombre = models.CharField(max_length=100)
	precio = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.IntegerField(default=0) #Cantidad disponible en almacen, empieza en 0

	def __str__(self):
		return f"{self.sku} - {self.nombre}"

class Estado(models.Model): #Modelo estado
	nombre = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.nombre
