from django.contrib import admin
from .models import Oportunidad

@admin.register(Oportunidad)
class OportunidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'cliente', 'valor_estimado', 'etapa', 'fecha_creacion', 'fecha_cierre',)
    search_fields = ('titulo', 'cliente__nombre', 'cliente__nif')
    list_filter = ('etapa', 'fecha_creacion', 'fecha_cierre')
