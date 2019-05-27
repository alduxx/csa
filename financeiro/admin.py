from django.contrib import admin

from .models import *


"""
Registros
"""
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['posicao', 'historico', 'origem', 'numero_documento', 'valor_formatado', 'saldo_no_dia_formatado']
    readonly_fields = list_display
    ordering = ['-posicao','saldo_no_dia']
    list_filter = ['posicao', 'historico']

admin.site.register(Registro, RegistroAdmin)
