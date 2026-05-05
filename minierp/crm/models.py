from django.db import models
from django.utils import timezone #Para trabajar con fechas teniendo en cuenta la zona horariade Django
from core.models import Cliente #Importo cliente porque cada oportunidad del crm pertenece a un cliente

class Oportunidad(models.Model): #Modelo principal del crm
    class Etapa(models.TextChoices): #Define las etapas posibles del pipeline usando TextChoices
        PROSPECCION = 'PRO', 'Prospección'
        PROPUESTA = 'PRP', 'Propuesta'
        NEGOCIACION = 'NEG', 'Negociación'
        GANADA = 'GAN', 'Cerrada Ganada'
        PERDIDA = 'PER', 'Cerrada Perdida'

    titulo = models.CharField(max_length=200) #Nombre de la oportunidad
    cliente = models.ForeignKey( #Relacion con cliente
        Cliente,
        on_delete=models.CASCADE, #Si se borra el cliente, tambien sus oportunidades
        related_name='oportunidades'
    )
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    etapa = models.CharField( #estado actual de la oportunidad
        max_length=3,
        choices=Etapa.choices, #limita los valores a los definidos arriba
        default=Etapa.PROSPECCION #por defecto empieza en prospeccion
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    def __str__(self): #representacion en texto del objeto
        return f"{self.titulo} - {self.cliente.nombre}"
    
    @property
    def dias_abierta(self): #propiedad calculada. No se guarda en bbdd, se calcula cuando se necesita
        if not self.fecha_creacion: #si no hay fecha de creacion devuelve 0
            return 0
        final = self.fecha_cierre if self.fecha_cierre else timezone.now() #si esta cerrada -> fecha de cierre, si sigue abierta-> fecha actual
        return (final - self.fecha_creacion).days #resta fechas y devuelve los dias que lleva abierta
    
    @property
    def esta_cerrada(self):
        return self.etapa in (self.Etapa.GANADA, self.Etapa.PERDIDA) #cerrada si ganada o perdida
    
    class Meta:
        verbose_name = 'Oportunidad' #Nombre en el admin
        verbose_name_plural = 'Oportunidades'
        ordering = ['-fecha_creacion'] #Orden por defecto, primero las recientes
