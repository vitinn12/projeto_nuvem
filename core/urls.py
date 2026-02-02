from django.urls import path
from usuarios import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar-produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('editar-produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('excluir-produto/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('detalhes-usuario/<int:id>/', views.detalhar_usuario, name='detalhar_usuario'),
    path('editar-usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
]