from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class EditarPerfilForm(forms.ModelForm):
    nome = forms.CharField(max_length=150, label='Nome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Usuario
        fields = ['time_favorito']  # Campo do modelo

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Inicializa os campos extras
        self.fields['email'].initial = user.email
        self.fields['nome'].initial = user.first_name
        self.user = user

    def save(self, commit=True):
        # Atualiza os campos do usuário
        self.user.first_name = self.cleaned_data['nome']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
        
        # Salva campos do perfil (se houver)
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile
