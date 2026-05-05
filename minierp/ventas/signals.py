from django.db.models.signals import post_save #Señal que se ejecuta despues de guardar un objeto
from django.dispatch import receiver #Decorador para registrar funciones como receptoras de señales
import logging #Para registrar errores o eventos
from .models import Pedido

logger = logging.getLogger(__name__) #Crea logger asociado a este archivo, para guardar errores en consola o fichero

@receiver(post_save, sender=Pedido) #Funcion que se ejecuta automaticamente cada vez que se guarda un pedido
def actualizar_stock_al_confirmar(sender, instance, **kwargs):
    """
    Cuando un pedido pasa a CONFIRMADO:
    - resta stock
    - si no hay stock suficiente -> error en log
    """
    if instance.estado.nombre == "CONFIRMADO": #Comprueba si el pedido esta en confirmado
        for linea in instance.lineas.all(): #Recorre todas las lineas
            producto = linea.producto #Obtiene el producto de la linea

            if producto.stock < linea.cantidad: #Sino hay suficiente stock ->
                logger.error( # <- error en el log
                    f"Stock insuficiente para el producto {producto.nombre}. "
                    f"Stock actual: {producto.stock}, requerido: {linea.cantidad}"
                )
                continue #No bloquea solo registra error
            #Restar stock
            producto.stock -= linea.cantidad
            producto.save()