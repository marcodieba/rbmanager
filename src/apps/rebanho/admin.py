
from django.contrib import admin
from .models import Fazenda, Animal, Quantidade, Movimento


class FazendaAdmin(admin.ModelAdmin):
	# fieldsets = [
	# 	(None, {'fields':['title','description','video','created_date']}),
	# ]
	# inlines = [ImagenEmpresaInline]
    pass

class AnimalAdmin(admin.ModelAdmin):
    pass

class MovimentoAdmin(admin.ModelAdmin):
    pass

class QuantidadeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Fazenda, FazendaAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Quantidade, QuantidadeAdmin)
admin.site.register(Movimento, MovimentoAdmin)
