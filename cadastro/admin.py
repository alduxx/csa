import string

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet

from .models import *


class FilterPrimeiraLetra(admin.SimpleListFilter):
    """
    Filtra pela primeira letra do nome e mostra listagem no painel da direita
    com a contagem por letra inicial
    """
    title = 'Letra Inicial'

    parameter_name = 'letter'
    letters = list(string.ascii_uppercase)
    model = None

    def lookups(self, request, model_admin):
        self.model = f"{model_admin}"
        #print(self.model)
        qs = model_admin.get_queryset(request)
        lookups = []
        for letter in self.letters:
            count = None
            if(self.model=="cadastro.CoagricultorPorCicloAdmin"):
                count = qs.filter(
                                 coagricultor__nome__istartswith=letter).count()
            elif(self.model=="cadastro.CoagricultorAdmin"):
                count = qs.filter(nome__istartswith=letter).count()
            elif(self.model=="cadastro.CestaAdmin"):
                count = qs.filter(
                   coagricultor__coagricultor__nome__istartswith=letter).count()

            if count:
                lookups.append((letter, '{} ({})'.format(letter, count)))
        return lookups

    def queryset(self, request, queryset):
        """
        Retorna o queryself filtrado
        """
        filter_val = self.value()
        if filter_val in self.letters:
            if(self.model=="cadastro.CoagricultorPorCicloAdmin"):
                return queryset.filter(
                                   coagricultor__nome__istartswith=self.value())
            elif(self.model=="cadastro.CoagricultorAdmin"):
                return queryset.filter(nome__istartswith=self.value())
            elif(self.model=="cadastro.CestaAdmin"):
                return queryset.filter(
                     coagricultor__coagricultor__nome__istartswith=self.value())


"""
Cesta
"""
class ItemDaCestaInline(admin.TabularInline):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra para mostrar resultados apenas do ciclo ativo
        """
        if db_field.name == "produto":
            kwargs["queryset"] = ProdutoPorCiclo.objects \
                                                      .filter(ciclo__ativo=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    model = ItemDaCesta


class CestaAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra para mostrar resultados apenas do ciclo ativo
        """
        if db_field.name == "coagricultor":
            kwargs["queryset"] = CoagricultorPorCiclo.objects.filter(
                                                        ciclo__ativo=True
                                        #ciclo__ativo=self.coagricultor.ciclo
                                                                    )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    model = Cesta
    list_display = ['coagricultor_nome', 'versao', 'valor_total', 'ciclo_nome']
    inlines = [ItemDaCestaInline]
    ordering = ['coagricultor__coagricultor__nome', 'coagricultor__ciclo',
                                                                      'versao']
    list_filter = [FilterPrimeiraLetra, 'coagricultor__ciclo']
    readonly_fields = ['valor_total']

admin.site.register(Cesta, CestaAdmin)


"""
Produto
"""
class ProdutoPorCicloInline(admin.TabularInline):
    model = ProdutoPorCiclo
    extra = 0
    ordering = ['produto__nome',]

class ProdutoAdmin(admin.ModelAdmin):
    model = Produto
    ordering = ['nome',]
    #list_filter = (FirstLetterListFilter,)

admin.site.register(Produto, ProdutoAdmin)


"""
Ponto de Convivência
"""
class PontoConvivenciaPorCicloInline(admin.TabularInline):
    model = PontoConvivenciaPorCiclo
    extra = 0

admin.site.register(PontoConvivencia)


"""
Coagricultor
"""
class CicloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'coagricultor_link', 'ativo']

    inlines = [
                ProdutoPorCicloInline,
                PontoConvivenciaPorCicloInline
              ]

class CestaDoMesInline(admin.TabularInline):
    model = CestaDoMes
    extra = 0

class CoagricultorPorCicloAdmin(admin.ModelAdmin):
    model = CoagricultorPorCiclo
    list_display = ['coagricultor', 'ciclo']
    ordering = ['ciclo','coagricultor__nome']
    list_filter = (FilterPrimeiraLetra,)
    inlines = [CestaDoMesInline]

class CoagricultorAdmin(admin.ModelAdmin):
    model = Coagricultor
    list_display = ['nome', 'identificador']
    ordering = ['nome']
    list_filter = (FilterPrimeiraLetra,)

admin.site.register(Ciclo, CicloAdmin)

admin.site.register(Coagricultor, CoagricultorAdmin)
admin.site.register(CoagricultorPorCiclo, CoagricultorPorCicloAdmin)
