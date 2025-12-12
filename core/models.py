from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from PIL import Image as PilImage
import os

# =======================
# COMMIT 1 + COMMIT 2
# Validação de tamanho máximo (5MB) + miniaturas automáticas
# =======================


# Início do app usuarios

class Usuario(AbstractUser):
    time_favorito = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

        
# Fim de usuario

def validar_tamanho_arquivo(arquivo):
    limite = 5 * 1024 * 1024  # 5 MB
    if arquivo.size > limite:
        raise ValidationError("O tamanho máximo permitido para o arquivo é 5 MB.")

# Início de mídia
class Definicao(models.Model):
    
    partida = models.ForeignKey(
        'Partida',  
        on_delete=models.CASCADE, 
        related_name="definicoes", 
        null=True, 
        blank=True
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="definicoes_usuario")
    jogo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=500, blank=True)
    criado_em = models.DateField(auto_now_add=True)

    # ======================================================
    # ADICIONE ESTE MÉTODO AQUI DENTRO DA CLASSE DEFINICAO
    # ======================================================
    def imagem_recente(self):
        """Retorna a primeira imagem (a mais nova) desta definição."""
        return self.imagens.all().order_by('-criado_em').first()
    # ======================================================

    def __str__(self):
        return f"{self.jogo} - {self.descricao or 'Sem descrição'}"


class Imagem(models.Model):
    # ESTE MODELO JÁ ESTAVA CORRETO. NÃO MUDAMOS NADA.
    # Ele se liga à Definicao, que agora (corretamente) se liga à Partida.
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="imagens"
    )
    arquivo = models.ImageField(upload_to="imagens/", validators=[validar_tamanho_arquivo])
    thumbnail = models.ImageField(upload_to="imagens/thumbnails/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Salva a imagem e gera miniatura automaticamente."""
        super().save(*args, **kwargs)
        if self.arquivo:
            try:
                caminho = self.arquivo.path
                img = PilImage.open(caminho)
                img.thumbnail((300, 300))
                thumb_dir = os.path.join(os.path.dirname(caminho), "thumbnails")
                os.makedirs(thumb_dir, exist_ok=True)
                thumb_path = os.path.join(thumb_dir, f"thumb_{os.path.basename(caminho)}")
                img.save(thumb_path)
                self.thumbnail.name = f"imagens/thumbnails/thumb_{os.path.basename(caminho)}"
                super().save(update_fields=["thumbnail"])
            except Exception as e:
                print(f"Erro ao gerar miniatura: {e}")

    def __str__(self):
        return f"Imagem da partida {self.definicao.id}"


class Video(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="videos"
    )
    arquivo = models.FileField(upload_to="videos/", validators=[validar_tamanho_arquivo])
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.id}"


class Audio(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="audios"
    )
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Áudio da partida {self.definicao.id}"
    


class Link(models.Model):
    # Alterar esta linha para permitir Links soltos (sem Definicao prévia)
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.SET_NULL, # SET_NULL para manter a integridade
        related_name="links",
        null=True,                # Permite ser NULL no DB
        blank=True                # Permite ser vazio no Admin/Form
    )
    # Novo campo para o nome do jogo
    nome_do_jogo = models.CharField(max_length=200, verbose_name="Nome do Jogo") 
    titulo = models.CharField(max_length=255, verbose_name="Título do Link", null=True, blank=True)
    url = models.URLField(max_length=2000, verbose_name="URL do Link (Ex: YouTube)")
    criado_em = models.DateTimeField(auto_now_add=True)
    
# Fim de Mídia

# Início do app partidas

class HistoricoPartida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historicos')
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"


class Jogador(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nome) if self.nome else "Jogador sem nome"


class Partida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='partidas')
    time_casa = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do time da casa")
    time_visitante = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do time visitante")
    adversario = models.CharField(max_length=100, blank=True, help_text="Nome do adversário (opcional)")
    data = models.DateTimeField(default=timezone.now)
    registro_externo_id = models.IntegerField(null=True, blank=True, help_text="ID do registro oficial da partida")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        casa = self.time_casa if self.time_casa else None
        visitante = self.time_visitante if self.time_visitante else None
        data_value = self.data.date() if self.data and hasattr(self.data, 'date') else ""
        if casa and visitante:
            return f"{casa} x {visitante} - {data_value}"
        elif self.adversario:
            return f"{self.adversario} - {data_value}"
        else:
            return f"Partida em {data_value}"



class Gol(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='gols')
    autor = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True)
    minuto = models.PositiveIntegerField(help_text="Minuto do gol", null=True, blank=True)

    def __str__(self):
        autor_nome = self.autor.nome if self.autor and hasattr(self.autor, 'nome') else "Autor desconhecido"
        minuto_text = f"{self.minuto}'" if self.minuto is not None else "minuto desconhecido"
        return f"Gol de {autor_nome} aos {minuto_text} - {self.partida}"


class AvaliacaoPartida(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Nota da partida (0 a 5)"
    )
    melhor_jogador = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='melhor_em_avaliacoes')
    pior_jogador = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='pior_em_avaliacoes')
    comentario_avaliacao = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usuario_text = self.usuario.username if self.usuario and hasattr(self.usuario, 'username') else "Anônimo"
        return f"Avaliação ({self.nota}) por {usuario_text} - {self.partida}"


class AvaliacaoEstadio(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estadio = models.CharField(max_length=100, blank=False)
    avaliacao_experiencia = models.IntegerField(
        choices=[
            (1, '★☆☆☆☆ - Ruim'),
            (2, '★★☆☆☆ - Fraca'),
            (3, '★★★☆☆ - Média'),
            (4, '★★★★☆ - Boa'),
            (5, '★★★★★ - Incrível'),
        ],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=False,
        default=3
    )
    comentario_estadio = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nome = self.usuario.username if self.usuario else "Anônimo"
        return f"{nome} - {self.avaliacao_experiencia} estrelas"


class Time(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class AvaliacaoTorcida(models.Model):
    # === CAMPOS NOVOS E ESSENCIAIS ===
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avaliacoes_torcida", null=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name="avaliacoes_torcida", null=True)
    # ================================

    time = models.CharField(max_length=100)
    comentario_torcida = models.TextField(blank=True, null=True)
    emocao = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    presenca = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String de representação melhorada
        user_nome = self.usuario.username if self.usuario else "Anônimo"
        return f"Avaliação de {self.time} (Partida {self.partida_id}) por {user_nome}"


# =======================
# COMMIT 4
# Commit vazio: adicionado comentários explicativos sem alterar a lógica
# =======================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome_completo = models.CharField(max_length=120)
    bio = models.TextField(blank=True, null=True)

    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)

    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)

    def __str__(self):
        return self.user.username
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from PIL import Image as PilImage
import os

# =======================
# COMMIT 1 + COMMIT 2
# Validação de tamanho máximo (5MB) + miniaturas automáticas
# =======================


# Início do app usuarios

class Usuario(AbstractUser):
    time_favorito = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

        
# Fim de usuario

def validar_tamanho_arquivo(arquivo):
    limite = 5 * 1024 * 1024  # 5 MB
    if arquivo.size > limite:
        raise ValidationError("O tamanho máximo permitido para o arquivo é 5 MB.")

# Início de mídia
class Definicao(models.Model):
    
    partida = models.ForeignKey(
        'Partida',  
        on_delete=models.CASCADE, 
        related_name="definicoes", 
        null=True, 
        blank=True
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="definicoes_usuario")
    jogo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=500, blank=True)
    criado_em = models.DateField(auto_now_add=True)

    # ======================================================
    # ADICIONE ESTE MÉTODO AQUI DENTRO DA CLASSE DEFINICAO
    # ======================================================
    def imagem_recente(self):
        """Retorna a primeira imagem (a mais nova) desta definição."""
        return self.imagens.all().order_by('-criado_em').first()
    # ======================================================

    def __str__(self):
        return f"{self.jogo} - {self.descricao or 'Sem descrição'}"


class Imagem(models.Model):
    # ESTE MODELO JÁ ESTAVA CORRETO. NÃO MUDAMOS NADA.
    # Ele se liga à Definicao, que agora (corretamente) se liga à Partida.
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="imagens"
    )
    arquivo = models.ImageField(upload_to="imagens/", validators=[validar_tamanho_arquivo])
    thumbnail = models.ImageField(upload_to="imagens/thumbnails/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Salva a imagem e gera miniatura automaticamente."""
        super().save(*args, **kwargs)
        if self.arquivo:
            try:
                caminho = self.arquivo.path
                img = PilImage.open(caminho)
                img.thumbnail((300, 300))
                thumb_dir = os.path.join(os.path.dirname(caminho), "thumbnails")
                os.makedirs(thumb_dir, exist_ok=True)
                thumb_path = os.path.join(thumb_dir, f"thumb_{os.path.basename(caminho)}")
                img.save(thumb_path)
                self.thumbnail.name = f"imagens/thumbnails/thumb_{os.path.basename(caminho)}"
                super().save(update_fields=["thumbnail"])
            except Exception as e:
                print(f"Erro ao gerar miniatura: {e}")

    def __str__(self):
        return f"Imagem da partida {self.definicao.id}"


class Video(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="videos"
    )
    arquivo = models.FileField(upload_to="videos/", validators=[validar_tamanho_arquivo])
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.id}"


class Audio(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="audios"
    )
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Áudio da partida {self.definicao.id}"
    


class Link(models.Model):
    # Alterar esta linha para permitir Links soltos (sem Definicao prévia)
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.SET_NULL, # SET_NULL para manter a integridade
        related_name="links",
        null=True,                # Permite ser NULL no DB
        blank=True                # Permite ser vazio no Admin/Form
    )
    # Novo campo para o nome do jogo
    nome_do_jogo = models.CharField(max_length=200, verbose_name="Nome do Jogo") 
    titulo = models.CharField(max_length=255, verbose_name="Título do Link", null=True, blank=True)
    url = models.URLField(max_length=2000, verbose_name="URL do Link (Ex: YouTube)")
    criado_em = models.DateTimeField(auto_now_add=True)
    
# Fim de Mídia

# Início do app partidas

class HistoricoPartida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historicos')
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"


class Jogador(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nome) if self.nome else "Jogador sem nome"


class Partida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='partidas')
    time_casa = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do time da casa")
    time_visitante = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do time visitante")
    adversario = models.CharField(max_length=100, blank=True, help_text="Nome do adversário (opcional)")
    data = models.DateTimeField(default=timezone.now)
    registro_externo_id = models.IntegerField(null=True, blank=True, help_text="ID do registro oficial da partida")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        casa = self.time_casa if self.time_casa else None
        visitante = self.time_visitante if self.time_visitante else None
        data_value = self.data.date() if self.data and hasattr(self.data, 'date') else ""
        if casa and visitante:
            return f"{casa} x {visitante} - {data_value}"
        elif self.adversario:
            return f"{self.adversario} - {data_value}"
        else:
            return f"Partida em {data_value}"



class Gol(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='gols')
    autor = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True)
    minuto = models.PositiveIntegerField(help_text="Minuto do gol", null=True, blank=True)

    def __str__(self):
        autor_nome = self.autor.nome if self.autor and hasattr(self.autor, 'nome') else "Autor desconhecido"
        minuto_text = f"{self.minuto}'" if self.minuto is not None else "minuto desconhecido"
        return f"Gol de {autor_nome} aos {minuto_text} - {self.partida}"


class AvaliacaoPartida(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Nota da partida (0 a 5)"
    )
    melhor_jogador = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='melhor_em_avaliacoes')
    pior_jogador = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='pior_em_avaliacoes')
    comentario_avaliacao = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usuario_text = self.usuario.username if self.usuario and hasattr(self.usuario, 'username') else "Anônimo"
        return f"Avaliação ({self.nota}) por {usuario_text} - {self.partida}"


class AvaliacaoEstadio(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estadio = models.CharField(max_length=100, blank=False)
    avaliacao_experiencia = models.IntegerField(
        choices=[
            (1, '★☆☆☆☆ - Ruim'),
            (2, '★★☆☆☆ - Fraca'),
            (3, '★★★☆☆ - Média'),
            (4, '★★★★☆ - Boa'),
            (5, '★★★★★ - Incrível'),
        ],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=False,
        default=3
    )
    comentario_estadio = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nome = self.usuario.username if self.usuario else "Anônimo"
        return f"{nome} - {self.avaliacao_experiencia} estrelas"


class Time(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class AvaliacaoTorcida(models.Model):
    # === CAMPOS NOVOS E ESSENCIAIS ===
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avaliacoes_torcida", null=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name="avaliacoes_torcida", null=True)
    # ================================

    time = models.CharField(max_length=100)
    comentario_torcida = models.TextField(blank=True, null=True)
    emocao = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    presenca = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String de representação melhorada
        user_nome = self.usuario.username if self.usuario else "Anônimo"
        return f"Avaliação de {self.time} (Partida {self.partida_id}) por {user_nome}"


# =======================
# COMMIT 4
# Commit vazio: adicionado comentários explicativos sem alterar a lógica
# =======================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome_completo = models.CharField(max_length=120)
    bio = models.TextField(blank=True, null=True)

    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)

    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)

    def __str__(self):
        return self.user.username
