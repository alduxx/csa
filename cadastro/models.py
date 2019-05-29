from decimal import *

from django.utils.html import format_html
from django.db import models

from financeiro.models import Registro


TWOPLACES = Decimal(10) ** -2                        # Forca duas casas decimais


class Ciclo(models.Model):
    nome = models.CharField(max_length=60)
    data_inicio = models.DateField(auto_now=False, auto_now_add=False)
    data_fim = models.DateField(auto_now=False, auto_now_add=False)
    dia_base = models.PositiveSmallIntegerField(default=1)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def coagricultor_link(self):
        return format_html("""<a href="/admin/cadastro/coagricultorporciclo/?
                           ciclo__id__exact={}">Coagricultores do {}</a>""",
                           self.id,
                           self.nome)

    coagricultor_link.short_description = "Coagricultores"


class Cesta(models.Model):
    """
    Coluna valor:
         Ainda que o valor total da cesta possa ser obtido via funcao
         get_valor_total_no_ciclo, essa conta é custosa e pode demorar para
         calcular para todos os itens, portanto o valor é atualizado via
         signal na alteracao cesta
     """

    coagricultor = models.ForeignKey("CoagricultorPorCiclo",
                                     on_delete=models.CASCADE)
    versao = models.PositiveSmallIntegerField(default=1)
    valor_total = models.DecimalField(max_digits=8,
                                      decimal_places=2,
                                      default=0.0)

    def __str__(self):
        return (f"""{self.coagricultor.coagricultor.nome} -
                {self.coagricultor.ciclo.nome} - versão {self.versao}""")

    @property
    def coagricultor_nome(self):
        return self.coagricultor.coagricultor.nome

    @property
    def ciclo_nome(self):
        return self.coagricultor.ciclo.nome

    def get_itens(self):
        return self.itens.all()

    def get_valor_total_no_ciclo(self):
        """
        Valor dos itens da cesta + os centavos referentes ao identificador
        """
        valor = Decimal(self.coagricultor.coagricultor.identificador * 0.01) \
                .quantize(TWOPLACES) # Centavos do identificador - decimal
                                     #                         com 2 casas
        for item in self.itens.all():
            if(item.cesta.coagricultor.ciclo.ativo == True):
                valor = valor + item.produto.valor

        return valor

    def get_registros_financeiros(self):
        return Registro.objects.filter(
            valor=self.valor_total,
            posicao__range=(self.coagricultor.ciclo.data_inicio,
                            self.coagricultor.ciclo.data_fim)
        ).order_by('posicao')



class CestaDoMes(models.Model):
    """
    É a versao da cesta (modelo Cesta) atribuida à um mês dentro do cicloself.
    """
    cesta = models.ForeignKey(Cesta, on_delete=models.CASCADE)
    coagricultor = models.ForeignKey("CoagricultorPorCiclo",
                                     related_name='itens',
                                     on_delete=models.CASCADE)
    mes = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return (f'{self.mes}/{self.cesta.ciclo_nome} - '
                 '{self.cesta.coagricultor_nome}')

    @property
    def coagricultor_nome(self):
        return self.cesta.coagricultor.coagricultor.nome


class ItemDaCesta(models.Model):
    cesta = models.ForeignKey("Cesta", related_name='itens',
                              on_delete=models.CASCADE)
    produto = models.ForeignKey("ProdutoPorCiclo", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.produto.produto.nome}'

    class Meta:
        verbose_name = 'Item da Cesta'
        verbose_name_plural = 'Itens da Cesta'

    @property
    def ciclo_nome(self):
        return self.cesta.coagricultor.ciclo.nome

    class Meta:
        verbose_name = 'Cesta do Mês'
        verbose_name_plural = 'Cestas do Mês'


class Coagricultor(models.Model):
    identificador = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Coagricultores'


class CoagricultorPorCiclo(models.Model):
    ciclo = models.ForeignKey("Ciclo", on_delete=models.CASCADE)
    coagricultor = models.ForeignKey("Coagricultor", on_delete=models.CASCADE)
    ponto_de_convivencia = models.ForeignKey("PontoConvivenciaPorCiclo",
                                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.coagricultor.nome}'

    class Meta:
        verbose_name = 'Coagricultor por Ciclo'
        verbose_name_plural = 'Coagricultores por Ciclo'
        ordering = ['coagricultor__nome']

    def get_itens(self):
        return self.itens

    def get_registros_financeiros(self):
        valores = []
        for i in range(6): # 0 - 5
            cesta_do_mes = CestaDoMes.objects \
                                     .get(coagricultor=self, mes=i+1)
            valores.append(cesta_do_mes.cesta.valor_total);

        distintos = list(set(valores))

        registros = []
        for valor in distintos:
            print(valor)
            registros.extend(
                Registro.objects.filter(
                    valor=valor,
                    posicao__range=(self.ciclo.data_inicio, self.ciclo.data_fim)
                ).order_by('posicao')
            )

        return registros


class PontoConvivencia(models.Model):
    nome = models.CharField(max_length=28)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Ponto de Convivência'
        verbose_name_plural = 'Pontos de Convivência'


class PontoConvivenciaPorCiclo(models.Model):
    ciclo = models.ForeignKey("Ciclo", on_delete=models.CASCADE)
    ponto_convivencia = models.ForeignKey("PontoConvivencia",
                                          on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ciclo.nome} - {self.ponto_convivencia.nome}'

    class Meta:
        verbose_name = 'Ponto de Convivência por Ciclo'
        verbose_name_plural = 'Pontos de Convivência por Ciclo'


class Produto(models.Model):
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome


class ProdutoPorCiclo(models.Model):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.produto.nome} - {self.valor}'

    class Meta:
        verbose_name = 'Produto por Ciclo'
        verbose_name_plural = 'Produtos por Ciclo'
        ordering = ['produto__nome']
