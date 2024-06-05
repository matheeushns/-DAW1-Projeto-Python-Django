from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Doador, Doacao
from .forms import DoadorForm, DoacaoForm, DoadorUpdateForm
from django.urls import reverse
import datetime

def cadastrar_doador(request):
    if request.method == 'POST':
        form = DoadorForm(request.POST)
        if form.is_valid():
            if Doador.objects.filter(cpf=form.cleaned_data['cpf']).exists():
                cpf=form.cleaned_data['cpf']
                messages.error(request, f'CPF {cpf} já cadastrado!')
            else:
                nome = form.cleaned_data['nome']
                form.save()
                messages.success(request, f'Doador(a) {nome} cadastrado(a) com sucesso!')
                form = DoadorForm()
                doadores = Doador.objects.all().order_by('codigo')
                context = {'form': form, 'doadores': doadores}
                return render(request, 'cadastrar_doador.html', context)
        else:
            messages.error(request, 'Erro ao cadastrar doador. Verifique os dados.')
    else:
        form = DoadorForm()
    
    doadores = Doador.objects.all().order_by('codigo')
    context = {'form': form, 'doadores': doadores}
    return render(request, 'cadastrar_doador.html', context)

def editar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if request.method == 'POST':
        form = DoadorForm(request.POST, instance=doador)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            form.save()
            messages.success(request, f"Doador(a) {doador.nome} editado(a) com sucesso.")
            return redirect(reverse('pesquisar_doador') + f'?nome={nome}&cpf={cpf}')
    else:
        form = DoadorForm(instance=doador)
    context = {'form': form, 'doador': doador}
    return render(request, 'editar_doador.html', context)

def excluir_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if request.method == 'POST':
        doador.situacao = 'INATIVO'
        doador.save()
        messages.success(request, f"O(A) doador(a) {doador.nome} foi excluído(a) com sucesso.")
        return redirect(reverse('pesquisar_doador') + f'?nome=''&cpf=''&tipo_sanguineo=Todos&rh=Todos')

    return render(request, 'excluir_doador.html', {'doador': doador})



def pesquisar_doador(request):
    doadores = None

    if request.method == 'GET':
        tipo_sanguineo = request.GET.get('tipo_sanguineo')
        rh = request.GET.get('rh')
        nome = request.GET.get('nome')
        cpf = request.GET.get('cpf')
        doadores = Doador.objects.filter(situacao='ATIVO').order_by('codigo')

        if tipo_sanguineo and tipo_sanguineo != 'Todos':
            doadores = doadores.filter(tipo_sanguineo=tipo_sanguineo)
        if rh and rh != 'Todos':
            doadores = doadores.filter(rh=rh)
        if nome:
            doadores = doadores.filter(nome__icontains=nome)
        if cpf:
            doadores = doadores.filter(cpf=cpf)

    context = {
        'doadores': doadores,
        'nome': nome,
        'cpf': cpf,
        'tipo_sanguineo': tipo_sanguineo,
        'rh': rh
    }

    if doadores is None or not doadores.exists():
        messages.error(request,'Não foram encontrados doadores com os critérios informados.')
        return render(request, 'pesquisar_doador.html', context)
    
    return render(request, 'pesquisar_doador.html', context)

def reativar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if doador.situacao == 'INATIVO':
        doador.situacao = 'ATIVO'
        doador.save()
        messages.success(request, f'O doador {doador.nome} teve o status alterado para "ATIVO".')
    
    return render(request, 'pesquisar_doador.html')

def main_page(request):
    return render(request, 'main_page.html')

def cadastrar_doacao(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)
    if request.method == 'POST':
        doacao_form = DoacaoForm(request.POST)
        doador_form = DoadorUpdateForm(request.POST, instance=doador)
        if doacao_form.is_valid() and doador_form.is_valid():
            doacao = doacao_form.save(commit=False)
            doacao.codigo_doador = doador
            doacao.save()
            doador = doador_form.save(commit=False)
            doador.tipo_rh_corretos = True
            doador.tipo_sanguineo = doador_form.cleaned_data['tipo_sanguineo']
            doador.rh = doador_form.cleaned_data['rh']
            doador.save()
            messages.success(request, f'A doação para o(a) doador(a) {doador.nome} foi realizada com sucesso!')
            return redirect('pesquisar_doador_para_doar')
        else:
            messages.error(request, 'Erro ao realizar doação. Verifique os dados.')
    else:
        doacao_form = DoacaoForm()
        doador_form = DoadorUpdateForm(instance=doador)
    
    context = {'doacao_form': doacao_form, 'doador_form': doador_form}
    return render(request, 'cadastrar_doacao.html', context)

def pesquisar_doador_para_doar(request):
    if request.method == 'GET':
        nome = request.GET.get('nome')
        cpf = request.GET.get('cpf')
        doadores = Doador.objects.filter(situacao='ATIVO').order_by('codigo')

        if nome:
            doadores = doadores.filter(nome__icontains=nome)
        if cpf:
            doadores = doadores.filter(cpf=cpf)

        context = {
            'doadores': doadores,
            'nome': nome,
            'cpf': cpf
            }
        
        if not doadores.exists():
            messages.error(request, 'Não foram encontrados doadores com os critérios informados.')
            return render(request, 'pesquisar_doador_para_doar.html', context)

        return render(request, 'pesquisar_doador_para_doar.html', context)
    
    doador_id = request.POST.get('doador_id')
    if doador_id:
        return redirect('cadastrar_doacao', doador_id=doador_id)
    
    return redirect('pesquisar_doador_para_doar')

def pesquisar_doacoes(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    doacoes = Doacao.objects.select_related('codigo_doador').order_by('data')

    if data_inicio:
        doacoes = doacoes.filter(data__gte=data_inicio)
    if data_fim:
        doacoes = doacoes.filter(data__lte=data_fim)

    if not doacoes.exists():
        messages.error(request, 'Não foram encontradas doações com os critérios informados.')
        doacoes = None

    context = {
        'doacoes': doacoes,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'pesquisar_doacoes.html', context)


def doacoes_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)
    doacoes = Doacao.objects.filter(codigo_doador=doador_id).order_by('-data')
    return render(request, 'doacoes_doador.html', {'doador': doador, 'doacoes': doacoes})