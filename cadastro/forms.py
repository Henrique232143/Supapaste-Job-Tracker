from decimal import (
    Decimal,
    InvalidOperation
)

from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

from .models import (
    Candidatura,
    Empresa,
    Cargo,
    LanguageSuggestion,
    normalizar_nome
)


class EmpresaForm(forms.ModelForm):

    website = forms.CharField(
        required=False,
        label=_("Site")
    )

    class Meta:
        model = Empresa

        fields = [
            "name",
            "website",
        ]

        labels = {
            "name": _("Empresa"),
            "website": _("Site"),
        }

    def clean_name(self):

        nome = self.cleaned_data["name"]

        nome = " ".join(
            nome.strip().split()
        )

        nome_normalizado = normalizar_nome(
            nome
        )

        if Empresa.objects.filter(
            name_normalized=nome_normalizado
        ).exists():

            raise forms.ValidationError(
                _("Essa empresa já está cadastrada.")
            )

        return nome

    def clean_website(self):

        website = self.cleaned_data.get(
            "website"
        )

        if not website:
            return ""

        website = website.strip()

        if not website.startswith(
            ("http://", "https://")
        ):
            website = "https://" + website

        validador_url = URLValidator()

        try:
            validador_url(website)

        except ValidationError:

            raise forms.ValidationError(
                _("Digite um endereço de site válido.")
            )

        return website


class CargoForm(forms.ModelForm):

    class Meta:
        model = Cargo

        fields = [
            "name",
        ]

        labels = {
            "name": _("Cargo"),
        }

    def clean_name(self):

        nome = self.cleaned_data["name"]

        nome = " ".join(
            nome.strip().split()
        )

        nome_normalizado = normalizar_nome(
            nome
        )

        if Cargo.objects.filter(
            name_normalized=nome_normalizado
        ).exists():

            raise forms.ValidationError(
                _("Esse cargo já está cadastrado.")
            )

        return nome

class CandidaturaForm(forms.ModelForm):

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),
        label=_("Empresa"),
        empty_label=_("Selecione uma empresa")
    )

    cargo_catalogo = forms.ModelChoiceField(
        queryset=Cargo.objects.none(),
        label=_("Cargo"),
        empty_label=_("Selecione um cargo")
    )

    salario = forms.CharField(
        required=False,
        label=_("Salário"),
        widget=forms.TextInput(
            attrs={
                "inputmode": "decimal",
                "placeholder": _("Ex.: 3.500,00")
            }
        )
    )

    class Meta:
        model = Candidatura

        fields = [
            "empresa",
            "data_candidatura",
            "salario",
            "link_vaga",
            "modalidade",
            "status",
            "observacoes",
            "ultimo_contato",
            "local_vaga",
        ]

        labels = {
            "empresa": _("Empresa"),
            "data_candidatura": _("Data da candidatura"),
            "link_vaga": _("Link da vaga"),
            "modalidade": _("Modalidade"),
            "status": _("Status"),
            "observacoes": _("Observações"),
            "ultimo_contato": _("Último contato"),
            "local_vaga": _("Local da vaga"),
        }

        widgets = {
            "data_candidatura": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "ultimo_contato": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "observacoes": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),
        }

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            "empresa"
        ].queryset = Empresa.objects.order_by(
            "name"
        )

        self.fields[
            "cargo_catalogo"
        ].queryset = Cargo.objects.order_by(
            "name"
        )

        self.order_fields([
            "empresa",
            "cargo_catalogo",
            "local_vaga",
            "data_candidatura",
            "salario",
            "link_vaga",
            "modalidade",
            "status",
            "observacoes",
            "ultimo_contato",
        ])
        
        if (
            self.instance
            and self.instance.pk
            and self.instance.cargo
        ):

            cargo_normalizado = normalizar_nome(
                self.instance.cargo
            )

            cargo_catalogo = (
                self.fields[
                    "cargo_catalogo"
                ].queryset
                .filter(
                    name_normalized=cargo_normalizado
                )
                .first()
            )

            if cargo_catalogo:

                self.initial[
                    "cargo_catalogo"
                ] = cargo_catalogo
            
        
    def clean_salario(self):

        valor = self.cleaned_data.get(
            "salario"
        )

        if not valor:
            return None

        valor = valor.strip()

        valor = (
            valor
            .replace("R$", "")
            .replace("r$", "")
            .replace(" ", "")
        )

        if not valor:
            return None

        if "," in valor and "." in valor:

            ultima_virgula = valor.rfind(
                ","
            )

            ultimo_ponto = valor.rfind(
                "."
            )

            if ultima_virgula > ultimo_ponto:

                valor = (
                    valor
                    .replace(".", "")
                    .replace(",", ".")
                )

            else:

                valor = valor.replace(
                    ",", ""
                )

        elif "," in valor:

            partes = valor.rsplit(
                ",",
                1
            )

            parte_decimal = partes[1]

            if len(parte_decimal) == 2:

                valor = (
                    partes[0].replace(
                        ",", ""
                    )
                    + "."
                    + parte_decimal
                )

            else:

                valor = valor.replace(
                    ",", ""
                )

        elif "." in valor:

            partes = valor.rsplit(
                ".",
                1
            )

            parte_decimal = partes[1]

            if len(parte_decimal) == 2:

                valor = (
                    partes[0].replace(
                        ".", ""
                    )
                    + "."
                    + parte_decimal
                )

            else:

                valor = valor.replace(
                    ".", ""
                )

        try:

            salario = Decimal(
                valor
            )

        except InvalidOperation:

            raise forms.ValidationError(
                _(
                    "Digite um salário válido. "
                    "Exemplo: 3.500,00"
                )
            )

        if salario < 0:

            raise forms.ValidationError(
                _("O salário não pode ser negativo.")
            )

        if salario > Decimal(
            "99999999.99"
        ):

            raise forms.ValidationError(
                _(
                    "Digite um salário dentro "
                    "de um valor válido."
                )
            )

        salario = salario.quantize(
            Decimal("0.01")
        )

        return salario

    def save(
        self,
        commit=True
    ):

        candidatura = super().save(
            commit=False
        )

        cargo = self.cleaned_data[
            "cargo_catalogo"
        ]

        candidatura.cargo = (
            cargo.name
        )

        if commit:
            candidatura.save()

        return candidatura


class StatusCandidaturaForm(
    forms.ModelForm
):

    class Meta:
        model = Candidatura

        fields = [
            "status",
        ]

        labels = {
            "status": _("Etapa do processo"),
        }

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "status-select"
                }
            )
        }


class CadastroForm(forms.ModelForm):

    senha = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Senha")
    )

    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Confirmar senha")
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "email",
        ]

        labels = {
            "first_name": _("Nome"),
            "email": _("E-mail"),
        }

    def clean(self):

        cleaned_data = super().clean()

        senha = cleaned_data.get(
            "senha"
        )

        confirmar_senha = cleaned_data.get(
            "confirmar_senha"
        )

        if (
            senha
            and confirmar_senha
            and senha != confirmar_senha
        ):

            raise forms.ValidationError(
                _("As senhas não coincidem.")
            )

        return cleaned_data


class LanguageSuggestionForm(
    forms.ModelForm
):

    class Meta:
        model = LanguageSuggestion

        fields = [
            "idioma",
        ]

        labels = {
            "idioma": _("Idioma"),
        }

        widgets = {
            "idioma": forms.TextInput(
                attrs={
                    "placeholder": _("Ex.: Francês"),
                    "maxlength": 100,
                    "required": True,
                }
            )
        }