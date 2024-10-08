from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.financeiro.models import Financeiro
from apps.financeiro.forms import FinanceiroForm
from datetime import date
from django.contrib import messages
from django.db.models import Sum

@login_required(login_url="admin/login/")
def financeiro(request):
    if request.method == 'POST':
        fazenda = request.POST.get('fazenda')
        datas = request.POST.getlist('data[]')
        nr_notas = request.POST.getlist('nr_nota[]')
        descricoes = request.POST.getlist('descricao[]')
        entradas = request.POST.getlist('entrada[]')
        saidas = request.POST.getlist('saida[]')

        for data, nr_nota, descricao, entrada, saida in zip(datas, nr_notas, descricoes, entradas, saidas):
            Financeiro.objects.create(
                fazenda_id=fazenda,
                data=data,
                nr_nota=nr_nota,
                descricao=descricao,
                entrada=entrada,
                saida=saida
            )
        #if form.is_valid():
        form = FinanceiroForm()
        #return render(request, 'financeiro.html', {'form': form})  # Redireciona para uma página de sucesso ou similar

    else:
        form = FinanceiroForm()

    return render(request, 'financeiro.html', {'form': form})

@login_required(login_url="admin/login/")
def editar_movimento(request, id):
    movimento = get_object_or_404(Financeiro, id=id)
    if request.method == 'POST':
        form = FinanceiroForm(request.POST, instance=movimento)
        if form.is_valid():
            form.save()
            return redirect('relfinanceiro')
    else:
        form = FinanceiroForm(instance=movimento)
    return render(request, 'editar_movimento.html', {'form': form})

@login_required(login_url="admin/login/")
def excluir_movimento(request, id):
    movimento = get_object_or_404(Financeiro, id=id)
    if request.method == 'POST':
        movimento.delete()
        messages.success(request, 'Movimento excluído com sucesso!')
        return redirect('relfinanceiro')
    return render(request, 'confirmar_exclusao.html', {'movimento': movimento})


@login_required(login_url="admin/login/")
def relfinanceiro(request):
    search = request.GET.get('search')
    filtro = request.GET.get('filtro')
    filtro_mes = request.GET.get('data_inicio')
    filtro_dia = request.GET.get('data_fim')
    dados = []

    #queryset = Financeiro.objects.all().order_by('fazenda')

    if search:
        filtro_descricao = Financeiro.objects.filter(descricao__icontains=search)
        filtro_nf = Financeiro.objects.filter(nr_nota__icontains=search)
        
        if filtro_descricao.exists():
            dados = filtro_descricao
        elif filtro_nf.exists():
            dados = filtro_nf
        else:
            dados = Financeiro.objects.filter(fazenda__fazenda__icontains=search)

    elif filtro and filtro_mes == '':
        dados = Financeiro.objects.filter(fazenda__fazenda__icontains=filtro).order_by('data')
        saldo = calcular_saldo(dados)

    elif filtro_mes and filtro_dia and filtro:
        dados = Financeiro.objects.filter(data__range=[filtro_mes, filtro_dia], fazenda__fazenda__icontains=filtro).order_by('data')
        saldo = calcular_saldo(dados)

    elif filtro_mes and filtro_dia:
        #filtro_dia = date.today()
        dados = Financeiro.objects.filter(data__range=[filtro_mes, filtro_dia]).order_by('data')
        saldo = calcular_saldo(dados)

    else:
        #for obj in queryset:
        #    dados.append({
        #        'data': obj.data,
        #        'fazenda': obj.fazenda,
        #        'nr_nota': obj.nr_nota,
        #        'descricao': obj.descricao,
        #        'entrada': obj.entrada,
        #        'saida': obj.saida,
        #        'id': obj.id
        #    })

        entrada_total = Financeiro.objects.aggregate(entrada=Sum('entrada'))['entrada'] or 0
        saida_total = Financeiro.objects.aggregate(saida=Sum('saida'))['saida'] or 0
        saldo_ = round(entrada_total - saida_total, 2)

        saldo = f"{saldo_:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    context = {
        'saldo': saldo,
        'dados': dados,
    }

    return render(request, 'relfinanceiro.html', context)

def calcular_saldo(dados):
    entrada = dados.aggregate(total_entrada=Sum('entrada'))['total_entrada'] or 0
    saida = dados.aggregate(total_saida=Sum('saida'))['total_saida'] or 0
    saldo = entrada - saida
    return f"{saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
