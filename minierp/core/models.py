from django.db import models

class Cliente(models.Model):
	nif = models.CharField(max_length=9, unique=True, verbose_name="NIF")
	nombre = models.CharField(max_length=100)
	email = models.EmailField(blank=True, null=True)

	def __str__(self):
		return f"{self.nombre} ({self.nif})"

class Producto(models.Model):
	sku = models.CharField(max_length=12, unique=True, verbose_name="SKU")
	nombre = models.CharField(max_length=100)
	precio = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.sku} - {self.nombre}"

class Estado(models.Model):
	nombre = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.nombre
