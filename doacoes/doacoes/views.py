from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Doador
from .forms import DoadorForm
from django.urls import reverse

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
    
    doadores = Doador.objects.all()
    context = {'form': form, 'doadores': doadores}
    return render(request, 'cadastrar_doador.html', context)

def editar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if request.method == 'POST':
        form = DoadorForm(request.POST, instance=doador)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doador(a) {doador.nome} editado(a) com sucesso.")
            return redirect(reverse('pesquisar_doador') + f'?nome={doador.nome}&cpf={doador.cpf}&tipo_sanguineo=Todos&rh=Todos')
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
        return redirect(reverse('pesquisar_doador') + f'?tipo_sanguineo=Todos&rh=Todos')

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

    if doadores is None or not doadores.exists():
        messages.error(request,'Não foram encontrados doadores com os critérios informados.')
        return render(request, 'pesquisar_doador.html')
    
    return render(request, 'pesquisar_doador.html', {'doadores': doadores})

def reativar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if doador.situacao == 'INATIVO':
        doador.situacao = 'ATIVO'
        doador.save()
        messages.success(request, f'O doador {doador.nome} teve o status alterado para "ATIVO".')
    
    return render(request, 'pesquisar_doador.html')

def main_page(request):
    return render(request, 'main_page.html')