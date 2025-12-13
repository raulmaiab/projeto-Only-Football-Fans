from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    # =========================
    # Emoções
    # =========================
    path('emocao/', views.home, name='emocao_index'),
    path('emocao/avaliacao/inicio/', views.avaliacao_inicio, name='avaliacao_inicio'),
    path('emocao/avaliar/<int:time_id>/', views.avaliar_time, name='avaliar_time'),
    path('emocao/avaliacao/anterior/', views.avaliacoes_anteriores, name='avaliacoes_anteriores'),
    path('emocao/nova-avaliacao/', views.nova_avaliacao, name='nova_avaliacao'),
    path('partida/<int:partida_id>/ver-avaliacao-torcida/', views.ver_avaliacao_torcida, name='ver_avaliacao_torcida'),

    # =========================
    # Partidas (ROTAS AJUSTADAS AQUI)
    # =========================
    
    # ROTA 1: Avaliar Torcida da Casa (time_index=1)
    # Sugestão: Use esta rota no botão "Avaliar Torcida" do histórico.
    path('partida/avaliar_torcida/<int:partida_id>/casa/', 
         views.avaliar_torcida, 
         {'time_index': 1}, 
         name='avaliar_torcida_primeiro'), # Renomeado de 'avaliar_torcida' para maior clareza

    # ROTA 2: Avaliar Torcida Visitante (time_index=2)
    # Uso de 'defaults' para passar o time_index, removendo o lambda.
    path('partida/avaliar_torcida/<int:partida_id>/visitante/', 
         views.avaliar_torcida, 
         {'time_index': 2}, 
         name='avaliar_torcida_segundo'),

    # Rota Antiga (Manter para evitar quebra de links antigos, mas a view agora sempre assume time_index=1)
    path('partida/avaliar_torcida/<int:partida_id>/', 
         views.avaliar_torcida, 
         {'time_index': 1}, # Força o time_index=1 para a URL sem índice
         name='avaliar_torcida'), 

    path('partidas/', views.lista_partidas, name='lista_partidas'),
    path('partidas/registrar/', views.registrar_partida, name='registrar_partida'),
    path('partidas/avaliar/<int:partida_id>/', views.avaliar_partida, name='avaliar_partida'),
    path('partidas/ver/<int:partida_id>/', views.ver_avaliacao, name='ver_avaliacao'),

    # =========================
    # Mídia
    # =========================
    path('midia/galeria/', views.galeria, name='galeria'),
    path('midia/adicionar/<int:partida_id>/', views.adicionar_midia, name='adicionar_midia'),
    path('midia/adicionar_link/<int:definicao_id>/', views.adicionar_link, name='adicionar_link'),
    path('midia/links/', views.lista_links, name='lista_links'),
    path('midia/links/cadastrar/', views.adicionar_link_page, name='adicionar_link_page'),

    # =========================
    # Usuários
    # =========================
    path('register/', views.register_view, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # =========================
    # Página inicial / Perfil
    # =========================
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
]