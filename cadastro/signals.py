from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cesta, CestaDoMes, Ciclo

def lista_meses(inicio, fim, dia_base):
    """
    Lista os meses distintos que estão no período entre data inicio e data fim a partir do dia dia_base
    """
    meses = []
    mes = 0
    while inicio <= fim:
        inicio += timedelta(days=1)
        if(mes != inicio.month and inicio.day > dia_base):
            mes = inicio.month
            meses.append(mes)

    return meses


@receiver(post_save, sender=Cesta)
def post_save_cesta(sender, instance, created, **kwargs):
    """
    Cria as cestas do mes default (v1) para o coagricultor
    """
    if created:
        ciclo_atual = Ciclo.objects.get(ativo=True)
        for i, mes in enumerate(lista_meses(ciclo_atual.data_inicio, ciclo_atual.data_fim, ciclo_atual.dia_base)):
            CestaDoMes.objects.create(
                cesta=instance,
                coagricultor=instance.coagricultor,
                mes=i+1
            )
