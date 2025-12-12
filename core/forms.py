from django import forms
from .models import UserProfile

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'nome_completo',
            'bio',
            'instagram',
            'twitter',
            'site',
            'foto_perfil',
        ]
