# forms.py (Adicionando campos de senha)

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

Usuario = get_user_model()

class EditarPerfilForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', required=False)
    
    # NOVOS CAMPOS DE SENHA (Opcional)
    new_password1 = forms.CharField(label='Nova Senha', required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirme a Senha', required=False, widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['first_name', 'time_favorito', 'email'] 

    # ... __init__ permanece o mesmo ...
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['first_name'].label = 'Nome'
        self.fields['email'].disabled = True 

    # NOVO MÉTODO DE VALIDAÇÃO DE SENHA
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:
            if new_password1 and not new_password2:
                self.add_error('new_password2', 'Confirme a nova senha.')
            elif not new_password1 and new_password2:
                self.add_error('new_password1', 'Digite a nova senha.')
            elif new_password1 != new_password2:
                raise ValidationError("As senhas não coincidem.")
        
        return cleaned_data
    
    # ATUALIZANDO O SAVE PARA TRATAR A SENHA
    def save(self, commit=True):
        user = super().save(commit=False)
        
        new_password = self.cleaned_data.get("new_password1")
        
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save() 
        
        return user