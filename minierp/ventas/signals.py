from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from .models import Pedido

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pedido)
def actualizar_stock_al_confirmar(sender, instance, **kwargs):
    """
    Cuando un pedido pasa a CONFIRMADO:
    - resta stock
    - si no hay stock suficiente -> error en log
    """
    if instance.estado.nombre == "CONFIRMADO":
        for linea in instance.lineas.all():
            producto = linea.producto

            if producto.stock < linea.cantidad:
                logger.error(
                    f"Stock insuficiente para el producto {producto.nombre}. "
                    f"Stock actual: {producto.stock}, requerido: {linea.cantidad}"
                )
                continue #No bloquea solo registra error
            #Restar stock
            producto.stock -= linea.cantidad
            producto.save()