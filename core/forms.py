# forms.py CORRIGIDO

from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class EditarPerfilForm(forms.ModelForm):
    # Campo 'nome' customizado para preencher first_name
    nome = forms.CharField(max_length=150, label='Nome', required=False) 
    
    # Removendo o campo 'email' daqui, pois ele já é um campo do modelo AbstractUser
    # e você o desabilitou no template. 
    # Deixar email na Meta é mais limpo.

    class Meta:
        model = Usuario
        # Incluímos 'first_name', 'time_favorito' e 'email' na Meta.
        # Mesmo que 'email' e 'first_name' sejam campos do modelo,
        # o Django vai tentar preenchê-los se forem definidos no formulário (o que faremos na inicialização).
        fields = ['time_favorito', 'email'] # time_favorito é o campo que queremos salvar via ModelForm

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

        # 1. Carregamento do Nome (usando first_name do modelo)
        self.fields['nome'].initial = self.user.first_name

        # 2. Desabilitar email (conforme seu template)
        self.fields['email'].disabled = True 
        # Carregamento do email (já é feito automaticamente por ser ModelForm, 
        # mas garantimos a inicialização, caso não esteja na Meta):
        # self.fields['email'].initial = self.user.email 

    def clean_nome(self):
        # Adicione validação, se necessário, mas para este caso, apenas retorna o valor
        return self.cleaned_data.get('nome')

    def save(self, commit=True):
        # 1. Obter a instância do usuário que está sendo salva (request.user)
        user = super().save(commit=False)

        # 2. Mapear o campo customizado 'nome' de volta para 'first_name' no modelo
        user.first_name = self.cleaned_data['nome']

        # 3. Salvar o objeto (que agora tem time_favorito e first_name atualizados)
        if commit:
            user.save()
        
        return user # Retorna a instância do usuário