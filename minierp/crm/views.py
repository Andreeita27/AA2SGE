from django.shortcuts import render #render para importar html con datos
from .models import Oportunidad #modelo oportunidad

def crm_dashboard(request): #Vista que muestra el dashboard del crm
    oportunidades = Oportunidad.objects.select_related('cliente').all() #Obtiene todas las oportunidades de la bd
    #select_related optimiza la consulta porque tambien trae los datos del cliente en la misma query

    total = oportunidades.count() #total de oportunidades
    ganadas = oportunidades.filter(etapa=Oportunidad.Etapa.GANADA).count() #ganadas
    tasa_conversion = round((ganadas / total) * 100, 2) if total > 0 else 0 #Calculo del kpi
    # el 2 redondea a 2 decimales
    # if total > 0 evita la division entre 0

    context = {
        'tasa_conversion': tasa_conversion, #kpi principal dle crm
        'total': total, #Total de oportunidades
        'ganadas': ganadas, #ganadas
        'oportunidades': oportunidades.order_by('-valor_estimado'), #lista ordenada por valor (de mas a menos)
        'moneda': 'EUR',
    }
    return render(request, 'crm/dashboard.html', context) #Renderiza el html pasando todos los datos al template
