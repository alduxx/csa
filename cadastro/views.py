from datetime import datetime, timedelta
from decimal import *

from django.shortcuts import render

from financeiro.models import Registro
from cadastro.models import CoagricultorPorCiclo, Cesta, CestaDoMes, Ciclo


TWOPLACES = Decimal(10) ** -2  # Forca duas casas decimais
HOJE = datetime.date(datetime.today())
# TODO: remover comentário abaixo utilizado apenas nos testes
HOJE = HOJE + timedelta(days=15)


def lista_meses(inicio, fim, dia_base):
    """
    Lista os meses distintos que estão no período entre
    data inicio e data fim a partir do dia dia_base
    """
    meses = []
    mes = 0
    while inicio <= fim:
        inicio += timedelta(days=1)
        if(mes != inicio.month and inicio.day > dia_base):
            mes = inicio.month
            meses.append(mes)

    return meses


def extrato_condensado(request):
    """
    Gera o extrato condensado
    """
    ciclo_atual = Ciclo.objects.get(ativo=True)
    lista_coag = CoagricultorPorCiclo.objects.filter(ciclo=ciclo_atual)
    meses = lista_meses(ciclo_atual.data_inicio, HOJE,
                        ciclo_atual.dia_base)

    valor_cesta_mes = dict()
    qtde_por_cesta = dict()
    for _coagricultor in lista_coag:
        #print(_coagricultor)
        valores_distintos = []
        # qtde_meses = 0
        for i, mes in enumerate(meses):
            # qtde_meses += 1
            try:
                cesta_do_mes = CestaDoMes.objects \
                                         .get(coagricultor=_coagricultor,
                                              mes=i+1)

                for cesta_do_mes in _coagricultor.get_itens().filter(mes=mes):
                    chave = "%d_%d" % (_coagricultor.coagricultor.identificador,
                                       cesta_do_mes.cesta.versao)
                    if chave in qtde_por_cesta:
                        qtde_por_cesta[chave] += 1
                    else:
                        qtde_por_cesta[chave] = 1
            except CestaDoMes.DoesNotExist:
                pass

    return render(request,
                  #'cadastro/extrato.html',
                  'cadastro/extrato_condensado.html',
                  {
                    'ciclo_atual': ciclo_atual,
                    'lista_coag': lista_coag,
                    'meses': meses,
                    #'qtde_meses': qtde_meses,
                    'qtde_meses': len(meses),
                    'hoje': HOJE
                  }
                )


def extrato(request):
    """
    Gera o extrato
    """
    ciclo_atual = Ciclo.objects.get(ativo=True)
    lista_coag = CoagricultorPorCiclo.objects.filter(ciclo=ciclo_atual)

    valor_cesta_mes = dict()
    qtde_por_cesta = dict()
    for _coagricultor in lista_coag:
        #print(_coagricultor)
        valores_distintos = []
        qtde_meses = 0
        for i, mes in enumerate(lista_meses(ciclo_atual.data_inicio,
                                            HOJE, ciclo_atual.dia_base)):
            # print(f' mes: {i+1}')
            qtde_meses += 1
            try:
                cesta_do_mes = CestaDoMes.objects \
                                         .get(coagricultor=_coagricultor,
                                              mes=i+1)

                for cesta_do_mes in _coagricultor.get_itens().filter(mes=mes):
                    chave = "%d_%d" % (_coagricultor.coagricultor.identificador,
                                       cesta_do_mes.cesta.versao)
                    if chave in qtde_por_cesta:
                        qtde_por_cesta[chave] += 1
                    else:
                        qtde_por_cesta[chave] = 1
            except CestaDoMes.DoesNotExist:
                pass

    return render(request,
                  'cadastro/extrato.html',
                  {
                    'ciclo_atual': ciclo_atual,
                    'lista_coag': lista_coag,
                    'qtde_meses': qtde_meses,
                    'hoje': HOJE
                  }
                )
