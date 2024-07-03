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
locale.setlocale(locale.LC_ALL, '')

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
            #query_total = Totais.objects.filter(fazenda=fazenda, animal=animal)

            if total_geral_filtro.exists():
                total_entrada = total_geral_filtro.aggregate(Sum('entrada'))['entrada__sum'] or 0
                total_saida = total_geral_filtro.aggregate(Sum('saida'))['saida__sum'] or 0
                total_soma = total_entrada - total_saida
             #   query_total.update(total_entrada=total_soma)
            else:
                total_soma = 0
                #Totais.objects.create(fazenda=fazenda, animal=animal, total_entrada=soma)

            Quantidade.objects.create(
                tipo_movimento=tipo_movimento,
                fazenda=fazenda,
                data=data,
                animal=animal,
                entrada=entrada,
                saida=saida,
                obs=obs
            )

        return render(request, 'rebanho.html', context)  # Redireciona para uma página de sucesso ou similar

    return render(request, 'rebanho.html', context)

# RELATORIO REBANHO
@login_required(login_url="admin/login/")
def relrebanho(request):
    hoje = date.today()
    semana = date.fromordinal(hoje.toordinal() - 6)
    semana_anterior = date.fromordinal(hoje.toordinal() - 12)
    fazendas = Fazenda.objects.all()
    rebanho = Animal.objects.all()
    dados = []

    queryset = Quantidade.objects.select_related('animal', 'fazenda')

    for fazenda in fazendas:
        total_p_fazenda = queryset.filter(fazenda=fazenda)
        total_fazenda_entrada = total_p_fazenda.aggregate(Sum('entrada'))['entrada__sum'] or 0
        total_fazenda_saida = total_p_fazenda.aggregate(Sum('saida'))['saida__sum'] or 0
        total_fazenda = total_fazenda_entrada - total_fazenda_saida

        for tipo_animal in rebanho:
            movimento_total = total_p_fazenda.filter(animal=tipo_animal)
            if movimento_total.exists():
                total_entrada_semana = movimento_total.filter(data__range=[semana, hoje]).aggregate(Sum('entrada'))['entrada__sum'] or 0
                total_saida_semana = movimento_total.filter(data__range=[semana, hoje]).aggregate(Sum('saida'))['saida__sum'] or 0
                data = [dt.data for dt in queryset]
                total_entrada = movimento_total.aggregate(Sum('entrada'))['entrada__sum'] or 0
                total_saida = movimento_total.aggregate(Sum('saida'))['saida__sum'] or 0
                total_anterior = total_entrada - total_saida - (total_entrada_semana - total_saida_semana)
                total = total_entrada - total_saida
            else:
                total_entrada_semana = 0
                total_saida_semana = 0
                total_anterior = 0
                total = 0

            dados.append({
                'data': data[-1],
                'fazenda_filtro': fazenda.fazenda,
                'animal': tipo_animal.animal,
                'total_entrada': total_entrada_semana,
                'total_saida': total_saida_semana,
                'faz': 'faz',
                'total_anterior': total_anterior,
                'total': total,
                'total_fazenda': total_fazenda
            })

    context = {
        'dados': dados,
    }

    return render(request, 'rebanho_imp.html', context)
