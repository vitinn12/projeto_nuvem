from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def cadastro (request):
    return render(request, 'cadastro.html')

def listar_usuarios(request):
    return render(request, 'listar_usuarios.html')