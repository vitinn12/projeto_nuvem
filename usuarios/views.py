import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Produto
from django.shortcuts import get_object_or_404

def index(request):
    produtos = Produto.objects.all().order_by('-id')

    token = request.session.get('access_token')
    email_logado = request.session.get('user_email')
    meu_id = None

    if token and email_logado:
        url_lista = "https://usuarioapi-production.up.railway.app/api/usuarios/"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url_lista, headers=headers)
            if response.status_code == 200:
                usuarios_da_api = response.json()
                for u in usuarios_da_api:
                    if u.get('email') == email_logado:
                        meu_id = u.get('id')
                        break
        except Exception as e:
            print(f"Erro ao conectar com a API: {e}")

    context = {
        'produtos': produtos,
        'meu_id': meu_id,
        'email_logado': email_logado,
        'login_sucesso': request.session.pop('abrir_token_uma_vez', False),
        'token_json': request.session.pop('dados_token_temp', None)
    }

    return render(request, 'index.html', context)
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        url = "https://usuarioapi-production.up.railway.app/api/login/"
        
        try:
            response = requests.post(url, json={"email": email, "password": password})
            if response.status_code == 200:
                dados = response.json()
                request.session['access_token'] = dados.get('access')
                request.session['user_email'] = email # Salvamos o email para busca posterior
                request.session['abrir_token_uma_vez'] = True
                request.session['dados_token_temp'] = dados
                return redirect('index')
        except: pass
    return render(request, 'login.html')

def cadastro(request):
    if request.method == "POST":
        payload = {
            "username": request.POST.get('email'),
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name')
        }
        url = "https://usuarioapi-production.up.railway.app/api/registro/"
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                return redirect('login')
            else:
                return render(request, 'cadastro.html', {'mensagem': f'Erro: {response.text}'})
        except Exception as e:
            return render(request, 'cadastro.html', {'mensagem': str(e)})
            
    return render(request, 'cadastro.html')

def detalhar_usuario(request, id):
    token = request.session.get('access_token')
    if not token: return redirect('login')

    url = f"https://usuarioapi-production.up.railway.app/api/usuarios/{id}/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return render(request, 'detalhes_usuario_api.html', {'usuario': response.json()})
    except: pass
    return redirect('index')

def editar_usuario(request, id):
    token = request.session.get('access_token')
    if not token:
        return redirect('login')

    url = f"https://usuarioapi-production.up.railway.app/api/usuarios/{id}/"
    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        novo_username = request.POST.get('username')
        novo_email = request.POST.get('email')
        
        payload = {
            "username": novo_username,
            "email": novo_email,
            "first_name": request.POST.get('first_name', ''),
            "last_name": request.POST.get('last_name', '')
        }
        
        try:
            response = requests.put(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                request.session['user_email'] = novo_email
                
                messages.success(request, "Alterações salvas com sucesso!")
                
                return redirect('detalhar_usuario_api', id=id)
            else:
                messages.error(request, "Erro ao atualizar: Verifique se os dados são válidos.")
        except Exception as e:
            messages.error(request, f"Erro de conexão: {e}")

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            usuario_atual = response.json()
        else:
            return redirect('index')
    except:
        return redirect('index')

    return render(request, 'editar_usuario_api.html', {'usuario': usuario_atual})

def cadastrar_produto(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        
        Produto.objects.create(nome=nome, preco=preco)
        messages.success(request, "Produto adicionado com sucesso!")
        return redirect('index')
    
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    if request.method == "POST":
        produto.nome = request.POST.get('nome')
        produto.preco = request.POST.get('preco')
        produto.save()
        messages.success(request, "Produto atualizado!")
        return redirect('produtos_home')
        
    return render(request, 'editar_produto.html', {'produto': produto})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.warning(request, "Produto removido!")
    return redirect('index')

def logout_view(request):
    request.session.flush()
    return redirect('index')