from django.test import TestCase

from django.core.exceptions import ValidationError

from .forms import CadastroForm, CandidaturaForm, CargoForm, EmpresaForm
from .models import Cargo, Empresa
from .perfil_usuario import PerfilUsuario
from django.contrib.auth.models import User


class FormsTests(TestCase):
    def cadastro_data(self, **changes):
        data = {
            "first_name": "Ana",
            "last_name": "Silva",
            "email": "ana@example.com",
            "cpf": "529.982.247-25",
            "senha": "Teste123!",
            "confirmar_senha": "Teste123!",
        }
        data.update(changes)
        return data

    def test_catalogos_validam_duplicados_e_permitem_edicao(self):
        for model, form_class in ((Empresa, EmpresaForm), (Cargo, CargoForm)):
            with self.subTest(model=model):
                instance = model.objects.create(name="Análise de Dados")
                form = form_class(data={"name": " analise  de dados "})
                self.assertFalse(form.is_valid())
                self.assertIn("name", form.errors)
                form = form_class(data={"name": instance.name}, instance=instance)
                self.assertTrue(form.is_valid(), form.errors)

    def test_cpf_normalizado(self):
        form = CadastroForm(data=self.cadastro_data())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["cpf"], "52998224725")

    def test_cpf_invalido(self):
        for cpf in ("11111111111", "52998224726", "abc", "5299822472"):
            with self.subTest(cpf=cpf):
                form = CadastroForm(data=self.cadastro_data(cpf=cpf))
                self.assertFalse(form.is_valid())
                self.assertIn("cpf", form.errors)

    def test_cpf_duplicado_com_mascara(self):
        user = User.objects.create_user(username="existente")
        PerfilUsuario.objects.create(usuario=user, cpf="52998224725")
        form = CadastroForm(data=self.cadastro_data())
        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors())

    def test_email_obrigatorio_e_compativel_com_username(self):
        for email in ("", "a" * 64 + "@" + "b" * 63 + "." + "c" * 30 + ".com"):
            form = CadastroForm(data=self.cadastro_data(email=email))
            self.assertFalse(form.is_valid())
            self.assertIn("email", form.errors)

    def test_confirmacao_preserva_espacos_da_senha(self):
        form = CadastroForm(data=self.cadastro_data(confirmar_senha="Teste123! "))
        self.assertFalse(form.is_valid())
        self.assertIn("confirmar_senha", form.errors)

    def test_salario_nao_finito(self):
        for salario in ("NaN", "sNaN", "Infinity", "-Infinity"):
            with self.subTest(salario=salario):
                form = CandidaturaForm()
                form.cleaned_data = {"salario": salario}
                with self.assertRaises(ValidationError):
                    form.clean_salario()
