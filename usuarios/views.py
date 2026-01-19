from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests


def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        payload = {
            "email": email,
            "password": password
        }
        
        url = "https://usuarioapi-production.up.railway.app/api/login/"
        
        try:
            response = requests.post(url, json=payload)
            dados_api = response.json()
            
            if response.status_code == 200:
                return JsonResponse({
                    "status": "sucesso",
                    "mensagem": "Login realizado com sucesso!",
                    "tokens": dados_api 
                }, status=200)
            else:
                return JsonResponse({
                    "status": "erro",
                    "detalhes": dados_api
                }, status=response.status_code)
                
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)
            
    return render(request, 'login.html')

def cadastro(request):
    mensagem = None
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        payload = {
            "username": email, 
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }

        url = "https://usuarioapi-production.up.railway.app/api/registro/" 
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 201:
                mensagem = "Usuário criado com sucesso!"
            else:

                mensagem = f"Erro no cadastro: {response.text}"
        except Exception as e:
            mensagem = f"Erro de conexão: {e}"
            
    return render(request, 'cadastro.html', {'mensagem': mensagem})
def listar_usuarios(request):
    return render(request, 'listar_usuarios.html')