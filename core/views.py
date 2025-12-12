from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import EditarPerfilForm

from .models import (
    AvaliacaoTorcida, AvaliacaoEstadio, Time, Partida, Imagem, Video, Audio,
    Definicao, Gol, AvaliacaoPartida, Jogador, Link
)

Usuario = get_user_model()


# ----------------------------
# Função auxiliar
# ----------------------------

def get_partidas_context(request):
    """
    Retorna o contexto de partidas e partidas avaliadas pelo usuário logado.
    Se o usuário não estiver logado, retorna listas vazias.
    """
    if not request.user.is_authenticated:
        return {"partidas": [], "partidas_avaliadas": set()}

    partidas = Partida.objects.filter(usuario=request.user).order_by("-data")
    avaliacoes = AvaliacaoPartida.objects.filter(usuario=request.user)
    partidas_avaliadas = {a.partida_id for a in avaliacoes}

    return {"partidas": partidas, "partidas_avaliadas": partidas_avaliadas}


# ----------------------------
# USUÁRIOS: login, logout, registro
# ----------------------------

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        time_favorito = request.POST.get('time_favorito') or ''
        avatar = request.FILES.get('avatar')

        if password != confirm_password:
            return render(request, 'usuarios/register.html', {'error': 'Senhas não coincidem'})
        if Usuario.objects.filter(username=username).exists():
            return render(request, 'usuarios/register.html', {'error': 'Usuário já existe'})
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'usuarios/register.html', {'error': 'Email já cadastrado'})

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            time_favorito=time_favorito,
            avatar=avatar
        )

        login(request, user)
        return redirect('core:home')

    return render(request, 'usuarios/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, 'usuarios/login.html')


def user_logout(request):
    logout(request)
    return redirect("core:login")


# ----------------------------
# PÁGINA INICIAL
# ----------------------------

def home(request):
    """Página inicial - redireciona para landing ou sistema"""
    if request.user.is_authenticated:
        partidas_registradas = Partida.objects.filter(usuario=request.user).count()
        estadios_avaliados = AvaliacaoEstadio.objects.filter(usuario=request.user).count()
        time_favorito = request.user.time_favorito
        
        context = {
            'partidas_registradas': partidas_registradas,
            'estadios_avaliados': estadios_avaliados,
            'time_favorito': time_favorito,
        }
        return render(request, 'home.html', context)
    else:
        # Se NÃO estiver logado, mostra a landing page
        return render(request, 'main.html')


# ----------------------------
# EMOÇÕES
# ----------------------------

@login_required(login_url='/login/')
def avaliar_torcida(request, partida_id, time_index=1):
    partida = get_object_or_404(Partida, id=partida_id)
    time = partida.time_casa if time_index == 1 else partida.time_visitante

    if request.method == 'POST':
        AvaliacaoTorcida.objects.create(
            time=request.POST.get('time'),
            comentario_torcida=request.POST.get('comentario'),
            emocao=request.POST.get('emocao'),
            presenca=request.POST.get('presenca'),
            
            # --- CAMPOS ADICIONADOS ---
            usuario=request.user,
            partida=partida
            # --------------------------
        )

        if time_index == 1:
            # Continua o fluxo para avaliar o segundo time (Time Visitante)
            # (Certifique-se que você tenha uma URL com name='avaliar_torcida_segundo' 
            #  apontando para esta view com time_index=2)
            return redirect('core:avaliar_torcida_segundo', partida_id=partida_id)
        else:
            # --- MUDANÇA NO REDIRECT ---
            # Após avaliar o segundo time, volta para a tela de 'ver_avaliacao'
            messages.success(request, "Avaliações das torcidas registradas com sucesso!")
            return redirect('core:ver_avaliacao', partida_id=partida.id) 

    context = {'time': time, 'partida': partida}
    context.update(get_partidas_context(request))
    return render(request, 'emocao/avaliar_torcida.html', context)


@login_required(login_url='/login/')
def avaliacao_inicio(request):
    context = {}
    context.update(get_partidas_context(request))
    return render(request, 'emocao/avaliacao_inicio.html', context)


@login_required(login_url='/login/')
def nova_avaliacao(request):
    if request.method == "POST":
        estadio_nome = request.POST.get("estadio")
        avaliacao_raw = request.POST.get("avaliacao")
        comentario = request.POST.get("comentario")

        # Validação mínima
        if not estadio_nome or not avaliacao_raw:
            return render(request, "emocao/nova_avaliacao.html", {
                "erro": "Preencha todos os campos obrigatórios."
            })

        try:
            avaliacao = int(avaliacao_raw)
        except ValueError:
            return render(request, "emocao/nova_avaliacao.html", {
                "erro": "A avaliação deve ser um número entre 1 e 5."
            })

        # Cria avaliação associada ao usuário logado
        AvaliacaoEstadio.objects.create(
            estadio=estadio_nome,
            avaliacao_experiencia=avaliacao,
            comentario_estadio=comentario,
            usuario=request.user
        )

        return render(request, "emocao/avaliacao_sucesso.html")

    context = {}
    context.update(get_partidas_context(request))
    return render(request, "emocao/nova_avaliacao.html", context)


@login_required(login_url='/login/')
def avaliacoes_anteriores(request):
    page_number = request.GET.get('page', 1)
    avaliacoes = AvaliacaoEstadio.objects.filter(usuario=request.user).order_by('-data_avaliacao')
    paginator = Paginator(avaliacoes, 1)
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    context.update(get_partidas_context(request))
    return render(request, "emocao/avaliacoes_anteriores.html", context)


def avaliar_time(request, time_id):
    time = get_object_or_404(Time, id=time_id)

    if request.method == "POST":
        comentario = request.POST.get("comentario")
        emocao = request.POST.get("emocao")
        presenca = request.POST.get("presenca")

        AvaliacaoTorcida.objects.create(
            comentario=comentario,
            emocao=emocao,
            presenca=presenca,
            time=time
        )

        proximo_time = Time.objects.filter(nome="Time 2").first()
        if proximo_time and time.nome == "Time 1":
            return redirect("avaliar_time", time_id=proximo_time.id)

        return redirect("resultado_avaliacoes")

    context = {"time": time}
    context.update(get_partidas_context(request))
    return render(request, "avaliacao_form.html", context)


def resultado_avaliacoes(request):
    avaliacoes = AvaliacaoTorcida.objects.all()
    context = {"avaliacoes": avaliacoes}
    context.update(get_partidas_context(request))
    return render(request, "emocao/resultado.html", context)

@login_required(login_url='/login/')
def ver_avaliacao_torcida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    
    # Pega as avaliações (espera-se 2) desta partida por este usuário
    avaliacoes = AvaliacaoTorcida.objects.filter(
        partida=partida, 
        usuario=request.user
    ).order_by('time') # Ordena pelo nome do time

    if not avaliacoes.exists():
        messages.error(request, "Você ainda não avaliou as torcidas desta partida.")
        # Volta para a tela anterior
        return redirect('core:ver_avaliacao', partida_id=partida.id)

    context = {
        "partida": partida,
        "avaliacoes": avaliacoes
    }
    context.update(get_partidas_context(request))
    # Renderiza o novo template que você pediu
    return render(request, "emocao/ver_ava_torcida.html", context)


# ----------------------------
# MÍDIA
# ----------------------------

@login_required(login_url='/login/')
def galeria(request):
    context = {
        "partidas": Partida.objects.filter(usuario=request.user).order_by("-data"),
        "definicoes": Definicao.objects.filter(usuario=request.user)
    }
    context.update(get_partidas_context(request))
    return render(request, "midia/galeria.html", context)

# ============================
# ADICIONAR MÍDIA (IMAGEM/VIDEO/AUDIO)
# ============================

# Em core/views.py

@login_required
def adicionar_midia(request, partida_id):
    # 1. Pega a partida (como antes)
    partida = get_object_or_404(Partida, id=partida_id, usuario=request.user)
    
    # --- INÍCIO DA CORREÇÃO ---
    # 2. Agora usamos a ForeignKey 'partida' em vez do campo 'jogo'
    definicao, _ = Definicao.objects.get_or_create(
        partida=partida,  # <-- ESTA É A CORREÇÃO REAL
        usuario=request.user,
        defaults={"jogo": str(partida), "descricao": ""} # Ainda salvamos o 'jogo' por segurança
    )
    # --- FIM DA CORREÇÃO ---

    if request.method == "POST":
        
        # O seu código original aqui estava CORRETO.
        # A Imagem só precisa da 'definicao'.
        if "imagem" in request.FILES:
            Imagem.objects.create(
                definicao=definicao, 
                arquivo=request.FILES["imagem"]
            )
        if "video" in request.FILES:
            Video.objects.create(
                definicao=definicao, 
                arquivo=request.FILES["video"]
            )
        if "audio" in request.FILES:
            Audio.objects.create(
                definicao=definicao, 
                arquivo=request.FILES["audio"]
            )
            
        messages.success(request, "Mídia adicionada com sucesso!")
        return redirect("core:galeria")

    context = {"partida": partida, "definicao": definicao}
    context.update(get_partidas_context(request))
    return render(request, "midia/adicionar_midia.html", context)

# ============================
# ADICIONAR LINK ASSOCIADO À DEFINIÇÃO
# ============================

@login_required
def adicionar_link(request, definicao_id):
    definicao = get_object_or_404(Definicao, pk=definicao_id, usuario=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        url = request.POST.get('url')

        if titulo and url:
            Link.objects.create(definicao=definicao, titulo=titulo, url=url)
            messages.success(request, f"Link '{titulo}' adicionado com sucesso!")
            # Pegando a partida correta para redirect
            partida = Partida.objects.filter(usuario=request.user, jogo=definicao.jogo).first()
            if partida:
                return redirect('core:adicionar_midia', partida_id=partida.id)
            else:
                return redirect('core:galeria')
        else:
            messages.error(request, "Título e URL são obrigatórios para adicionar o link.")

    context = {
        'definicao': definicao,
        'page_title': f'Adicionar Link à Partida {definicao.jogo}',
    }
    context.update(get_partidas_context(request))
    return render(request, 'midia/adicionar_link.html', context)

# ============================
# ADICIONAR LINK SOLTO (SEM DEFINIÇÃO)
# ============================

@login_required
def adicionar_link_page(request):
    if request.method == 'POST':
        nome_do_jogo = request.POST.get('nome_do_jogo')
        url = request.POST.get('url')

        if nome_do_jogo and url:
            Link.objects.create(nome_do_jogo=nome_do_jogo, url=url)
            messages.success(request, f"Link de {nome_do_jogo} cadastrado com sucesso!")
            return redirect('core:lista_links')
        else:
            messages.error(request, "Nome do Jogo e URL são obrigatórios.")

    context = {'page_title': 'Cadastrar Novo Link de Jogo'}
    context.update(get_partidas_context(request))
    return render(request, 'midia/adicionar_link_page.html', context)

# ============================
# LISTA DE LINKS
# ============================

@login_required
def lista_links(request):
    user_definicoes = Definicao.objects.filter(usuario=request.user)
    links = Link.objects.filter(
        Q(definicao__in=user_definicoes) | Q(definicao__isnull=True)
    ).order_by('-criado_em')

    context = {'links': links, 'page_title': 'Links de Replay e Mídia'}
    context.update(get_partidas_context(request))
    return render(request, 'midia/lista_links.html', context)


# ----------------------------
# PARTIDAS
# ----------------------------

@login_required(login_url='/login/')
def lista_partidas(request):
    partidas = Partida.objects.filter(usuario=request.user).order_by("-data")
    avaliacoes = AvaliacaoPartida.objects.filter(usuario=request.user)
    partidas_avaliadas = {a.partida_id for a in avaliacoes}
    return render(request, "partidas/lista_partidas.html", {
        "partidas": partidas,
        "partidas_avaliadas": partidas_avaliadas
    })


@login_required(login_url='/login/')
def registrar_partida(request):
    times = Time.objects.all()

    if request.method == "POST":
        time_casa_nome = request.POST.get("time_casa")
        time_visitante_nome = request.POST.get("time_visitante")
        data = request.POST.get("data")

        if request.user.is_authenticated:
            Partida.objects.create(
                usuario=request.user,
                time_casa=time_casa_nome,
                time_visitante=time_visitante_nome,
                data=data
            )

        return redirect("core:lista_partidas")

    context = {"times": times}
    context.update(get_partidas_context(request))
    return render(request, "partidas/registrar_partida.html", context)


@login_required(login_url='/login/')
def avaliar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.user.is_authenticated:
        ja_avaliou = AvaliacaoPartida.objects.filter(partida=partida, usuario=request.user).exists()
        if ja_avaliou:
            messages.warning(request, "Você já avaliou esta partida!")
            return redirect("core:lista_partidas")

    if request.method == "POST":
        nota = int(request.POST.get("nota", 0))
        melhor_nome = request.POST.get("melhor_jogador", "").strip()
        pior_nome = request.POST.get("pior_jogador", "").strip()
        comentario = request.POST.get("comentario", "")

        melhor_jogador = Jogador.objects.get_or_create(nome=melhor_nome)[0] if melhor_nome else None
        pior_jogador = Jogador.objects.get_or_create(nome=pior_nome)[0] if pior_nome else None

        AvaliacaoPartida.objects.create(
            partida=partida,
            usuario=request.user if request.user.is_authenticated else None,
            nota=nota,
            melhor_jogador=melhor_jogador,
            pior_jogador=pior_jogador,
            comentario_avaliacao=comentario
        )

        messages.success(request, "Avaliação registrada com sucesso!")
        return redirect("core:lista_partidas")

    context = {"partida": partida}
    context.update(get_partidas_context(request))
    return render(request, "partidas/avaliar_partida.html", context)


def ver_avaliacao(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    avaliacao = AvaliacaoPartida.objects.filter(partida=partida, usuario=request.user).first()

    if not avaliacao:
        messages.error(request, "Você ainda não avaliou esta partida.")
        return redirect("core:lista_partidas")

    # --- NOVA LÓGICA ---
    # A sua view 'avaliar_torcida' tem lógica para time_index=1 e time_index=2.
    # Vamos assumir que "avaliado" significa que existem 2 registros (um para cada time).
    avaliacoes_torcida_count = AvaliacaoTorcida.objects.filter(
        partida=partida, 
        usuario=request.user
    ).count()

    # Se a contagem for 2 ou mais, consideramos que a avaliação foi feita.
    torcida_ja_avaliada = avaliacoes_torcida_count >= 2
    # ---------------------

    context = {
        "avaliacao": avaliacao, 
        "partida": partida,
        "torcida_ja_avaliada": torcida_ja_avaliada  # <-- Passa a variável para o template
    }
    context.update(get_partidas_context(request))
    return render(request, "partidas/ver_avaliacao.html", context)


def registrar_gols(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == "POST":
        autores = request.POST.getlist("autor")
        minutos = request.POST.getlist("minuto")

        for autor, minuto in zip(autores, minutos):
            if autor and minuto:
                Gol.objects.create(partida=partida, autor=autor, minuto=minuto)

        return redirect("detalhe_partida", partida_id=partida.id)

    context = {"partida": partida}
    context.update(get_partidas_context(request))
    return render(request, "registrar_gols.html", context)


# ----------------------------
# PERFIL
# ----------------------------

@login_required
def editar_perfil(request):
    profile, _ = request.user.userprofile.get_or_create(user=request.user)

    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('core:perfil')
    else:
        form = EditarPerfilForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'user': request.user,
        # Adicione outros itens de contexto conforme necessário, por exemplo:
        # 'profile': profile,
    }
    return render(request, 'perfil.html', context)
