
from django.contrib import admin
from .models import Financeiro

@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = ['fazenda', 'descricao', 'entrada', 'saida', 'data']
	# fieldsets = [
	# 	(None, {'fields':['title','description','video','created_date']}),
	# ]
	# inlines = [ImagenEmpresaInline]



