class EditarPerfilForm(forms.ModelForm):
    email = forms.EmailField()
    nome = forms.CharField(max_length=150)

    class Meta:
        model = UserProfile
        fields = ['time']  # só o campo do profile

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['email'].initial = user.email
        self.fields['nome'].initial = user.first_name
        self.user = user

    def save(self, commit=True):
        profile = super().save(commit=False)

        # salva no User
        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data['nome']
        if commit:
            self.user.save()
            profile.save()
        return profile
