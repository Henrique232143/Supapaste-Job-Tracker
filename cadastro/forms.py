from django import forms
from .models import Candidatura
from django.contrib.auth.models import User


class CandidaturaForm(forms.ModelForm):

    class Meta:
        model = Candidatura

        fields = [
            'empresa',
            'cargo',
            'data_candidatura',
            'salario',
            'link_vaga',
            'modalidade',
            'status',
            'observacoes',
            'ultimo_contato',
        ]

        widgets = {
            'data_candidatura': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'ultimo_contato': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'observacoes': forms.Textarea(
                attrs={'rows': 4}
            ),
        }


class CadastroForm(forms.ModelForm):

    senha = forms.CharField(
        widget=forms.PasswordInput
    )

    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'email',
        ]

        labels = {
            'first_name': 'Nome',
            'email': 'E-mail',
        }

    def clean(self):

        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:

            raise forms.ValidationError(
                'As senhas não coincidem.'
            )

        return cleaned_data