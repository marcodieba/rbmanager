
from django.contrib import admin
from .models import Financeiro

@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    pass
	# fieldsets = [
	# 	(None, {'fields':['title','description','video','created_date']}),
	# ]
	# inlines = [ImagenEmpresaInline]



