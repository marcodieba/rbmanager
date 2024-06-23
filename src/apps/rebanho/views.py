from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from apps.rebanho.models import Animal, Quantidade, Fazenda
from apps.rebanho.forms import *
from datetime import date
from django.db.models import Count, Sum, F, Q
import locale
import json
locale.setlocale( locale.LC_ALL, '' )



# ARIA DE ENTRADA E SAIDA DE ANIMAIS
@login_required(login_url="admin/login/")
def rebanho(request):
    form = RebanhoForm()
    hoje = date.today()
    semana = date.fromordinal(hoje.toordinal() - 6)
    rebanho = Quantidade.objects.all()
    context = {
        'form': form,
    }
    
    if request.method == "POST":
        fazenda_id = request.POST.get('fazenda')
        tipo_movimento_id = request.POST.get('tipo_movimento')
        data = request.POST.get('data')
        animais_ids = request.POST.getlist('animal')
        entradas = request.POST.getlist('entrada[]')
        saidas = request.POST.getlist('saida[]')
        observacoes = request.POST.getlist('obs[]')

        # Obtenha as instâncias correspondentes
        fazenda = Fazenda.objects.get(id=fazenda_id)
        tipo_movimento = Movimento.objects.get(id=tipo_movimento_id)

        for animal_id, entrada, saida, obs in zip(animais_ids, entradas, saidas, observacoes):
            animal = Animal.objects.get(id=animal_id)
            soma = int(entrada) - int(saida)
            total_geral_filtro = Quantidade.objects.filter(fazenda=fazenda, animal=animal)
            query_total = Totais.objects.filter(fazenda=fazenda, animal=animal)

            for total in query_total:
                if total_geral_filtro:
                    total_entrada = total_geral_filtro.aggregate(q=Sum('entrada'))
                    total_saida = total_geral_filtro.aggregate(q=Sum('saida'))
                    total_soma = total_entrada['q'] - total_saida['q']
                    query_total.update(total_entrada=total_soma)
                else:
                    total_soma = 0
                    totais = Totais(fazenda=fazenda, animal=animal, total_entrada=soma)
                    totais.save()

            Quantidade.objects.create(
                tipo_movimento=tipo_movimento,
                fazenda=fazenda,
                data=data,
                animal=animal,
                entrada=entrada,
                saida=saida,
                obs=obs
            )

        return render(request, 'rebanho.html', context)   # Redireciona para uma página de sucesso ou similar

    return render(request, 'rebanho.html', context)


#RELATORIO REBANHO
@login_required(login_url="admin/login/")
def relrebanho(request):
    hoje = date.today()
    semana = date.fromordinal(hoje.toordinal()-6)
    semana_anterior = date.fromordinal(hoje.toordinal() - 12)
    fazendas = Fazenda.objects.all()
    rebanho = Animal.objects.all() 
    dados = []

    for obj in fazendas:
        total_p_fazenda = Quantidade.objects.filter(fazenda__fazenda=obj.fazenda)
        queryset = Quantidade.objects.select_related('animal', 'fazenda')
        total_fazenda = total_p_fazenda.aggregate(q=Sum('entrada'))['q'] - total_p_fazenda.aggregate(q=Sum('saida'))['q']
        
        for tipo_animal in rebanho:
            tipo = [obj.animal for obj in Quantidade.objects.filter(animal=tipo_animal, fazenda=obj)]
            movimento_total = Quantidade.objects.filter(animal=tipo_animal, fazenda=obj)
            if tipo_animal in tipo:
                for value in movimento_total:
                    total_entrada_semana = movimento_total.filter(data__range=[semana, hoje]).aggregate(q=Sum('entrada'))['q']
                    total_saida_semana = movimento_total.filter(data__range=[semana, hoje]).aggregate(q=Sum('saida'))['q']
                    total = movimento_total.aggregate(q=Sum('entrada'))['q'] - movimento_total.aggregate(q=Sum('saida'))['q']
                    if total_entrada_semana or total_saida_semana:
                        entrada_atual = total_entrada_semana
                        saida_atual = total_saida_semana
                        total_anterior = movimento_total.aggregate(q=Sum('entrada'))['q'] - movimento_total.aggregate(q=Sum('saida'))['q'] - (total_entrada_semana - total_saida_semana)
                    else:
                        entrada_atual = 0
                        saida_atual = 0
                        total_anterior = movimento_total.aggregate(q=Sum('entrada'))['q'] - movimento_total.aggregate(q=Sum('saida'))['q']
            else:
                entrada_atual = 0
                saida_atual = 0
                total_anterior = 0
                total = 0        

                   
            for i in queryset:
                dados_ = {
                            'data':hoje,
                            'fazenda_filtro':obj.fazenda,
                            'animal':tipo_animal.animal,
                            'total_entrada':entrada_atual,
                            'total_saida':saida_atual,
                            'faz':'faz',
                            'total_anterior': total_anterior,
                            'total':total,
                            'total_fazenda':total_fazenda
                            }

            dados.append(dados_)

    context = {
        'dados':dados,
        # 'soma_saida':soma_saida,
        # 'soma_entrada':soma_entrada,
    }

    return render(request, 'rebanho_imp.html', context)

