from django.db import models
import locale


class Registro(models.Model):
    posicao = models.DateField(auto_now=False, auto_now_add=False)
    historico = models.CharField(max_length=28)
    origem = models.CharField(max_length=6)
    numero_documento = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_no_dia = models.DecimalField(max_digits=10, decimal_places=2)
    hash = models.CharField(max_length=32, editable=False)

    def __str__(self):
        return f'{self.posicao} - {self.valor}'

    @property
    def valor_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        valor = locale.currency(self.valor, grouping=True, symbol=True)
        return valor

    valor_formatado.fget.short_description = u"Valor"

    @property
    def saldo_no_dia_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        valor = locale.currency(self.saldo_no_dia, grouping=True, symbol=True)
        return valor

    saldo_no_dia_formatado.fget.short_description = u"Saldo no dia"
