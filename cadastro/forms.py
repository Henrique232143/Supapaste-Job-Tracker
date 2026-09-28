import re

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

from .perfil_usuario import PerfilUsuario


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

        consulta = Empresa.objects.filter(
            name_normalized=nome_normalizado
        )

        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():

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
        nome = " ".join(self.cleaned_data["name"].split())
        consulta = Cargo.objects.filter(
            name_normalized=normalizar_nome(nome)
        )

        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
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
            "salario": _("Salário"),
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

        if not salario.is_finite():
            raise forms.ValidationError(
                _("Digite um salário válido. Exemplo: 3.500,00")
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


# ============================================================
# CADASTRO DE USUÁRIO
# ============================================================

class CadastroForm(forms.ModelForm):
    
    senha = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
        label=_("Senha")
    )

    confirmar_senha = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
        label=_("Confirmar senha")
    )

    cpf = forms.CharField(
        max_length=14,
        label=_("CPF"),
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "maxlength": "14",
                "placeholder": "000.000.000-00",
                "autocomplete": "off"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        labels = {
            "first_name": _("Nome"),
            "last_name": _("Sobrenome"),
            "email": _("E-mail"),
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "autocomplete": "given-name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "autocomplete": "family-name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "username"
                }
            ),
        }

    def clean_first_name(self):

        nome = self.cleaned_data.get(
            "first_name"
        )

        nome = " ".join(
            nome.strip().split()
        )

        if not nome:

            raise forms.ValidationError(
                _("Informe seu nome.")
            )

        return nome

    def clean_last_name(self):

        sobrenome = self.cleaned_data.get(
            "last_name"
        )

        sobrenome = " ".join(
            sobrenome.strip().split()
        )

        if not sobrenome:

            raise forms.ValidationError(
                _("Informe seu sobrenome.")
            )

        return sobrenome

    def clean_email(self):

        email = self.cleaned_data.get(
            "email"
        )

        email = email.strip().lower()

        return email

    def clean_cpf(self):

        cpf = self.cleaned_data.get(
            "cpf"
        )

        # Remove pontos, traço e qualquer outro caractere
        # que não seja número.
        cpf = re.sub(
            r"\D",
            "",
            cpf
        )

        # CPF precisa ter exatamente 11 números.
        if len(cpf) != 11:

            raise forms.ValidationError(
                _("Digite um CPF válido.")
            )

        # Impede CPFs como:
        # 00000000000
        # 11111111111
        # 22222222222
        if cpf == cpf[0] * 11:

            raise forms.ValidationError(
                _("Digite um CPF válido.")
            )

        # =====================================================
        # PRIMEIRO DÍGITO VERIFICADOR
        # =====================================================

        soma = sum(
            int(cpf[i]) * (10 - i)
            for i in range(9)
        )

        resto = soma % 11

        digito_1 = (
            0
            if resto < 2
            else 11 - resto
        )

        if digito_1 != int(cpf[9]):

            raise forms.ValidationError(
                _("Digite um CPF válido.")
            )

        # =====================================================
        # SEGUNDO DÍGITO VERIFICADOR
        # =====================================================

        soma = sum(
            int(cpf[i]) * (11 - i)
            for i in range(10)
        )

        resto = soma % 11

        digito_2 = (
            0
            if resto < 2
            else 11 - resto
        )

        if digito_2 != int(cpf[10]):

            raise forms.ValidationError(
                _("Digite um CPF válido.")
            )

        return cpf

    def clean_senha(self):

        senha = self.cleaned_data.get(
            "senha"
        )

        if not senha:

            return senha

        requisitos_faltantes = []

        if len(senha) < 6:

            requisitos_faltantes.append(
                "pelo menos 6 caracteres"
            )

        if not any(
            caractere.isupper()
            for caractere in senha
        ):

            requisitos_faltantes.append(
                "uma letra maiúscula"
            )

        if not any(
            caractere.islower()
            for caractere in senha
        ):

            requisitos_faltantes.append(
                "uma letra minúscula"
            )

        if not any(
            caractere.isdigit()
            for caractere in senha
        ):

            requisitos_faltantes.append(
                "um número"
            )

        if not any(
            not caractere.isalnum()
            for caractere in senha
        ):

            requisitos_faltantes.append(
                "um caractere especial"
            )

        if requisitos_faltantes:

            if len(requisitos_faltantes) == 1:

                mensagem = (
                    "A senha precisa ter "
                    + requisitos_faltantes[0]
                    + "."
                )

            elif len(requisitos_faltantes) == 2:

                mensagem = (
                    "A senha precisa incluir "
                    + requisitos_faltantes[0]
                    + " e "
                    + requisitos_faltantes[1]
                    + "."
                )

            else:

                mensagem = (
                    "A senha precisa incluir "
                    + ", ".join(
                        requisitos_faltantes[:-1]
                    )
                    + " e "
                    + requisitos_faltantes[-1]
                    + "."
                )

            raise forms.ValidationError(
                _(mensagem)
            )

        return senha

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

            self.add_error(
                "confirmar_senha",
                _("As senhas não coincidem.")
            )

        email = cleaned_data.get(
            "email"
        )

        cpf = cleaned_data.get(
            "cpf"
        )

        duplicidade = False

        # Verifica e-mail existente.
        if email:

            if User.objects.filter(
                username__iexact=email
            ).exists():

                duplicidade = True

        # Verifica CPF existente.
        if cpf:

            if PerfilUsuario.objects.filter(
                cpf=cpf
            ).exists():

                duplicidade = True

        # IMPORTANTE:
        # Não informamos se foi o CPF ou o e-mail que já existe.
        # Isso evita revelar quais dados possuem uma conta.
        if duplicidade:

            raise forms.ValidationError(
                _(
                    "Não foi possível concluir o cadastro "
                    "com os dados informados. "
                    "Verifique seus dados e tente novamente."
                )
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
