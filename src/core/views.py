from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from apps.rebanho.models import Animal, Quantidade, Fazenda
from apps.financeiro.models import Financeiro
from apps.rebanho.forms import *
from datetime import date
from django.db.models import Count, Sum, F, Q
import locale
import json
locale.setlocale( locale.LC_ALL, '' )

#@login_required(login_url="admin/login/")
def controle(request):
    data = date.today()
    ano = request.GET.get('filter_ano')
    mes = request.GET.get('filter_mes')
    grafico_venda = []
    grafico_data = []
    meses_ano = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #
  
    fazenda_nome = []
  
    # for obj in meses_ano:
    entrada = Quantidade.objects.filter(data__year=ano, data__month__gt=0, tipo_movimento_id=4)
    # mes_1 = entrada.annotate(entrada_fazenda=Sum('entrada'))
    # # mes_1.append(entrada)
    # for ob in mes_1:
       
    #     fazenda_nome.append({'fazenda':{f"{ob.fazenda.fazenda}":f"{ob.entrada}"}})
  
    for consulta in meses_ano:
        rvm = Quantidade.objects.filter(data__year=ano, data__month=consulta)
        if rvm:
            grafico_venda.append(rvm.aggregate(saida=Sum('saida'))['saida'])
        else:
            grafico_venda.append('0')
        # print(grafico_venda)
    
    animais = Quantidade.objects.filter(data__year=ano).order_by('fazenda')
     
    
    vendas_mes = 0
    vendas_ano = 0
    mes = Financeiro.objects.filter(data__year=ano)
    gastos = 0
    mortes = 0

    nascimentos_femea_1 = 0
    nascimentos_femea_2 = 0
    nascimentos_femea_3 = 0
    nascimentos_femea_4 = 0
    nascimentos_femea_5 = 0
    nascimentos_femea_6 = 0
    nascimentos_femea_7 = 0
    nascimentos_femea_8 = 0
    nascimentos_femea_9 = 0
    nascimentos_femea_10 = 0
    nascimentos_femea_11 = 0
    nascimentos_femea_12 = 0

    nascimentos_macho_1 = 0
    nascimentos_macho_2 = 0
    nascimentos_macho_3 = 0
    nascimentos_macho_4 = 0
    nascimentos_macho_5 = 0
    nascimentos_macho_6 = 0
    nascimentos_macho_7 = 0
    nascimentos_macho_8 = 0
    nascimentos_macho_9 = 0
    nascimentos_macho_10 = 0
    nascimentos_macho_11 = 0
    nascimentos_macho_12 = 0
    nascimentos_macho = 0
    data_nascimento_1 = ''
    data_nascimento_2 = ''
    data_nascimento_3 = ''
    data_nascimento_4 = ''
    data_nascimento_5 = ''
    data_nascimento_6 = ''
    data_nascimento_7 = ''
    data_nascimento_8 = ''
    data_nascimento_9 = ''
    data_nascimento_10 = ''
    data_nascimento_11 = ''
    data_nascimento_12 = ''
    for obj in mes:
        # total_entrada = Financeiro.objects.aggregate(entrada=Sum('entrada'))
        gastos = float(gastos) + float(obj.saida)
    # gastos = locale.currency(gastos, grouping=True ) valor como moeda
    gastos = gastos
    # print(gasto)
    for venda in animais:
        if venda.tipo_movimento_id == 1:
            vendas_mes = vendas_mes + venda.saida
        if venda.tipo_movimento_id == 3:
            mortes = mortes + venda.saida
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 1:
            nascimentos_femea_1 = nascimentos_femea_1 + venda.entrada
            data_nascimento_1 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 1:
            nascimentos_macho_1 = nascimentos_macho_1 + venda.entrada
            data_nascimento_1 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 2:
            nascimentos_femea_2 = nascimentos_femea_2 + venda.entrada
            data_nascimento_2 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 2:
            nascimentos_macho_2 = nascimentos_macho_2 + venda.entrada
            data_nascimento_2 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 3:
            nascimentos_femea_3 = nascimentos_femea_3 + venda.entrada
            data_nascimento_3 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 3:
            nascimentos_macho_3 = nascimentos_macho_3 + venda.entrada
            data_nascimento_3 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 4:
            nascimentos_femea_4 = nascimentos_femea_4 + venda.entrada
            data_nascimento_4 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 4:
            nascimentos_macho_4 = nascimentos_macho_4 + venda.entrada
            data_nascimento_4 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 5:
            nascimentos_femea_5 = nascimentos_femea_5 + venda.entrada
            data_nascimento_5 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 5:
            nascimentos_macho_5 = nascimentos_macho_5 + venda.entrada
            data_nascimento_5 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 6:
            nascimentos_femea_6 = nascimentos_femea_6 + venda.entrada
            data_nascimento_6 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 6:
            nascimentos_macho_6 = nascimentos_macho_6 + venda.entrada
            data_nascimento_6 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 7:
            nascimentos_femea_7 = nascimentos_femea_7 + venda.entrada
            data_nascimento_7 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 7:
            nascimentos_macho_7 = nascimentos_macho_7 + venda.entrada
            data_nascimento_7 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 8:
            nascimentos_femea_8 = nascimentos_femea_8 + venda.entrada
            data_nascimento_8 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 8:
            nascimentos_macho_8 = nascimentos_macho_8 + venda.entrada
            data_nascimento_8 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 9:
            nascimentos_femea_9 = nascimentos_femea_9 + venda.entrada
            data_nascimento_9 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 9:
            nascimentos_macho_9 = nascimentos_macho_9 + venda.entrada
            data_nascimento_9 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 10:
            nascimentos_femea_10 = nascimentos_femea_10 + venda.entrada
            data_nascimento_10 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 10:
            nascimentos_macho_10 = nascimentos_macho_10 + venda.entrada
            data_nascimento_10 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 11:
            nascimentos_femea_11 = nascimentos_femea_11 + venda.entrada
            data_nascimento_11 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 11:
            nascimentos_macho_11 = nascimentos_macho_11 + venda.entrada
            data_nascimento_11 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 1 and venda.data.month == 12:
            nascimentos_femea_12 = nascimentos_femea_12 + venda.entrada
            data_nascimento_12 = venda.data
        if venda.tipo_movimento_id == 4 and venda.animal_id == 2 and venda.data.month == 12:
            nascimentos_macho_12 = nascimentos_macho_12 + venda.entrada
            data_nascimento_12 = venda.data
     # = [obj.saida for obj in rvm]

    # lista_mes = [ for obj in rvm]
    # print(grafico_venda)
    

    grafico_data =['Jan', 'Fev', 'Mar', 'Mai', 'Abr', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    context = {
                # 'total_entrada':total_entrada,
                'gastos': gastos,
                'vendas_ano':vendas_ano,
                'vendas_mes':vendas_mes,
                'fazenda_nome':fazenda_nome,
                'nascimentos_femea_1':nascimentos_femea_1,
                'nascimentos_femea_2':nascimentos_femea_2,
                'nascimentos_femea_3':nascimentos_femea_3,
                'nascimentos_femea_4':nascimentos_femea_4,
                'nascimentos_femea_5':nascimentos_femea_5,
                'nascimentos_femea_6':nascimentos_femea_6,
                'nascimentos_femea_7':nascimentos_femea_7,
                'nascimentos_femea_8':nascimentos_femea_8,
                'nascimentos_femea_9':nascimentos_femea_9,
                'nascimentos_femea_10':nascimentos_femea_10,
                'nascimentos_femea_11':nascimentos_femea_11,
                'nascimentos_femea_12':nascimentos_femea_12,
                'nascimentos_macho_1':nascimentos_macho_1,
                'nascimentos_macho_2':nascimentos_macho_2,
                'nascimentos_macho_3':nascimentos_macho_3,
                'nascimentos_macho_4':nascimentos_macho_4,
                'nascimentos_macho_5':nascimentos_macho_5,
                'nascimentos_macho_6':nascimentos_macho_6,
                'nascimentos_macho_7':nascimentos_macho_7,
                'nascimentos_macho_8':nascimentos_macho_8,
                'nascimentos_macho_9':nascimentos_macho_9,
                'nascimentos_macho_10':nascimentos_macho_10,
                'nascimentos_macho_11':nascimentos_macho_11,
                'nascimentos_macho_12':nascimentos_macho_12,
                'data_nascimento_1' : data_nascimento_1,
                'data_nascimento_2' : data_nascimento_2,
                'data_nascimento_3' : data_nascimento_3,
                'data_nascimento_4' : data_nascimento_4,
                'data_nascimento_5' : data_nascimento_5,
                'data_nascimento_6' : data_nascimento_6,
                'data_nascimento_7' : data_nascimento_7,
                'data_nascimento_8' : data_nascimento_8,
                'data_nascimento_9' : data_nascimento_9,
                'data_nascimento_10' : data_nascimento_10,
                'data_nascimento_11' : data_nascimento_11,
                'data_nascimento_12' : data_nascimento_12,
                # 'nascimentos_femea_8':nascimentos_femea_8,
                # 'nascimentos_femea_9':nascimentos_femea_9,
                # 'nascimentos_femea_10':nascimentos_femea_10,
                'nascimentos_macho':nascimentos_macho,
                # 'data_nascimento':data_nascimento,
                'animais':animais,
                'mortes':mortes,
                'grafico_venda':json.dumps(grafico_venda),
                'grafico_data':json.dumps(grafico_data),
              }
    return render(request, 'controle.html', context)
