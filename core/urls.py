
from django.contrib import admin
from django.urls import path
from usuarios.views import index, login, cadastro, logout_view, detalhar_usuario, editar_usuario, editar_produto, excluir_produto, cadastrar_produto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logout/', logout_view, name='logout'),
    path('usuarios/<int:id>/', detalhar_usuario, name='detalhar_usuario_api'),
    path('usuarios/editar/<int:id>/', editar_usuario, name='editar_usuario_api'),
    path('produtos/editar/<int:id>/', editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:id>/', excluir_produto, name='excluir_produto'),    
    path('produtos/cadastrar/', cadastrar_produto, name='cadastrar_produto'),

]
