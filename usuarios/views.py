import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto

def index(request):
    produtos = Produto.objects.all().order_by('-id')
    token = request.session.get('access_token')
    email_logado = request.session.get('user_email')
    meu_id = None

    if token and email_logado:
        # Busca a lista para encontrar o ID do usuário logado pelo e-mail
        url_lista = "https://usuarioapi-production.up.railway.app/api/usuarios/"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url_lista, headers=headers)
            if response.status_code == 200:
                usuarios_api = response.json()
                for u in usuarios_api:
                    if u.get('email') == email_logado:
                        meu_id = u.get('id')
                        break
        except:
            pass

    context = {
        'produtos': produtos,
        'meu_id': meu_id,
        'login_sucesso': request.session.pop('abrir_token_uma_vez', False),
        'token_json': request.session.pop('dados_token_temp', None)
    }
    return render(request, 'index.html', context)

def cadastro(request):
    if request.method == "POST":
        payload = {
            "username": request.POST.get('username'),
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name')
        }
        url = "https://usuarioapi-production.up.railway.app/api/registro/"
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                messages.success(request, "Conta criada! Agora você pode entrar.")
                return redirect('login')
            else:
                messages.error(request, f"Erro no cadastro: {response.text}")
        except:
            messages.error(request, "Erro ao conectar com o servidor de registro.")
            
    return render(request, 'cadastro.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        url = "https://usuarioapi-production.up.railway.app/api/login/"
        
        try:
            payload = {"email": email, "password": password}
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                dados = response.json()
                request.session['access_token'] = dados.get('access')
                request.session['user_email'] = email
                request.session['abrir_token_uma_vez'] = True
                request.session['dados_token_temp'] = dados
                messages.success(request, "Login realizado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, "E-mail ou senha incorretos.")
        except:
            messages.error(request, "Erro de conexão durante o login.")
            
    return render(request, 'login.html')

def cadastrar_produto(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        preco = request.POST.get('preco')
        Produto.objects.create(nome=nome, categoria=categoria, preco=preco)
        messages.success(request, "Produto cadastrado internamente!")
    return redirect('index')

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        produto.nome = request.POST.get('nome')
        produto.categoria = request.POST.get('categoria')
        produto.preco = request.POST.get('preco')
        produto.save()
        messages.success(request, "Produto atualizado!")
        return redirect('index')
    return render(request, 'editar_produto.html', {'produto': produto})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.warning(request, "Produto removido com sucesso!")
    return redirect('index')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def detalhar_usuario(request, id):
    token = request.session.get('access_token')
    url = f"https://usuarioapi-production.up.railway.app/api/usuarios/{id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    usuario = response.json() if response.status_code == 200 else None
    return render(request, 'detalhes_usuario_api.html', {'usuario': usuario})

def editar_usuario(request, id):
    token = request.session.get('access_token')
    url = f"https://usuarioapi-production.up.railway.app/api/usuarios/{id}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    if request.method == "POST":
        payload = {
            "username": request.POST.get('username'),
            "email": request.POST.get('email'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name')
        }
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == 200:
            request.session['user_email'] = payload['email']
            messages.success(request, "Perfil atualizado!")
            return redirect('detalhar_usuario', id=id)
            
    response = requests.get(url, headers=headers)
    usuario = response.json()
    return render(request, 'editar_usuario_api.html', {'usuario': usuario})