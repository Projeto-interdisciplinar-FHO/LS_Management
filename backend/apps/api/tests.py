"""Testes da API REST (apps/api) e da autenticação.

Rodar a partir de backend/:
    python manage.py test
"""
from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.health.animal_health.models import AnimalHealth
from apps.health.vaccination_groups.models import VaccinationGroup
from apps.health.vaccination_plans.models import VaccinationPlan
from apps.health.vaccinations.models import Vaccination
from apps.health.vaccines.models import Vaccine
from apps.herd.breeds.models import Breed
from apps.herd.cattle.models import Bull, Cow
from apps.movements.movement_types.models import MovementType
from apps.production.weight_history.models import WeightHistory
from apps.reproduction.models import Insemination
from core.permissions import ADMINISTRADOR, OPERADOR, papel_de


class BaseAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.senha = "SenhaForte#2026"
        cls.admin = User.objects.create_superuser("admin", "admin@ls.com", cls.senha)
        cls.operador = User.objects.create_user("operador", "op@ls.com", cls.senha)
        cls.operador.groups.add(Group.objects.get(name=OPERADOR))

        cls.raca = Breed.objects.create(name="Holandesa")
        cls.vaca1 = Cow.objects.create(name="Mimosa", breed=cls.raca, register_number=1)
        cls.vaca2 = Cow.objects.create(name="Estrela", breed=cls.raca, register_number=2)

    def setUp(self):
        self.client = APIClient()

    def autenticar(self, usuario):
        self.client.force_authenticate(user=usuario)


class AutenticacaoTests(BaseAPITestCase):
    def test_api_exige_autenticacao(self):
        resposta = self.client.get("/cows/")
        self.assertEqual(resposta.status_code, 401)

    def test_login_devolve_tokens_e_papel(self):
        for rota in ("/api/token/", "/authentication/token/"):
            resposta = self.client.post(rota, {"username": "admin", "password": self.senha}, format="json")
            self.assertEqual(resposta.status_code, 200, rota)
            self.assertIn("access", resposta.data)
            self.assertIn("refresh", resposta.data)
            self.assertEqual(resposta.data["papel"], ADMINISTRADOR)

    def test_login_com_senha_errada(self):
        resposta = self.client.post("/api/token/", {"username": "admin", "password": "errada"}, format="json")
        self.assertEqual(resposta.status_code, 401)

    def test_token_jwt_e_aceito_nas_rotas(self):
        login = self.client.post("/api/token/", {"username": "operador", "password": self.senha}, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        self.assertEqual(self.client.get("/cows/").status_code, 200)

    def test_papeis(self):
        self.assertEqual(papel_de(self.admin), ADMINISTRADOR)
        self.assertEqual(papel_de(self.operador), OPERADOR)


class UsuariosTests(BaseAPITestCase):
    def test_operador_nao_lista_usuarios(self):
        self.autenticar(self.operador)
        self.assertEqual(self.client.get("/users/").status_code, 403)

    def test_admin_cadastra_usuario_sem_expor_senha(self):
        self.autenticar(self.admin)
        resposta = self.client.post(
            "/users/",
            {"username": "novo", "password": self.senha, "papel": OPERADOR},
            format="json",
        )
        self.assertEqual(resposta.status_code, 201, resposta.data)
        self.assertNotIn("password", resposta.data)
        self.assertTrue(User.objects.get(username="novo").check_password(self.senha))

    def test_cadastro_publico_cria_admin_e_permite_login(self):
        resposta = self.client.post(
            "/users/signup/",
            {
                "username": "visitante.campo",
                "first_name": "Visitante",
                "last_name": "Campo",
                "email": "visitante@ls.com",
                "password": self.senha,
            },
            format="json",
        )
        self.assertEqual(resposta.status_code, 201, resposta.data)
        usuario = User.objects.get(username="visitante.campo")
        self.assertEqual(papel_de(usuario), ADMINISTRADOR)
        self.assertTrue(usuario.is_staff)

        login = self.client.post(
            "/api/token/",
            {"username": "visitante.campo", "password": self.senha},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data["papel"], ADMINISTRADOR)


class RotasTests(BaseAPITestCase):
    """Garante que toda rota usada pelo frontend responde."""

    ROTAS = [
        "breeds", "quadrants", "classes", "bulls", "cows", "animals",
        "movement_types", "animal_movements", "birth_occurrences",
        "inseminations", "births", "vaccines", "vaccination_groups",
        "vaccination_plans", "vaccinations", "veterinary_occurrences",
        "animal_health", "foods", "feedings", "feeding_plans", "milking",
        "milk_production_history", "weight_history",
    ]

    def test_listagens_respondem(self):
        self.autenticar(self.operador)
        for rota in self.ROTAS:
            with self.subTest(rota=rota):
                self.assertEqual(self.client.get(f"/{rota}/").status_code, 200)

    def test_animals_e_alias_de_cows(self):
        self.autenticar(self.operador)
        cows = self.client.get("/cows/").data
        animals = self.client.get("/animals/").data
        self.assertEqual(cows, animals)


class CrudAnimalTests(BaseAPITestCase):
    def test_criar_editar_e_excluir_animal(self):
        self.autenticar(self.admin)
        criado = self.client.post(
            "/animals/",
            {"name": "Malhada", "breed": self.raca.id, "register_number": 3},
            format="json",
        )
        self.assertEqual(criado.status_code, 201, criado.data)
        pk = criado.data["id"]

        editado = self.client.patch(f"/animals/{pk}/", {"status": "sold"}, format="json")
        self.assertEqual(editado.status_code, 200)
        self.assertEqual(Cow.objects.get(pk=pk).status, "sold")

        self.assertEqual(self.client.delete(f"/animals/{pk}/").status_code, 204)
        self.assertFalse(Cow.objects.filter(pk=pk).exists())

    def test_excluir_animal_com_plano_sanitario_e_inseminacao(self):
        self.autenticar(self.admin)
        vaca = Cow.objects.create(name="Pérola", breed=self.raca, register_number=99)
        touro = Bull.objects.create(name="Trovão", breed=self.raca, register_number=199)
        vacina = Vaccine.objects.create(name="Febre aftosa")
        grupo = VaccinationGroup.objects.create(name="Plano sanitário - Pérola", animal=vaca)
        VaccinationPlan.objects.create(
            vaccination_group=grupo, vaccine=vacina, periodicity=180, total_doses=2
        )
        Insemination.objects.create(mother=vaca, father=touro, date=date(2026, 10, 1))

        resposta = self.client.delete(f"/animals/{vaca.id}/")
        self.assertEqual(resposta.status_code, 204)
        self.assertFalse(Cow.objects.filter(pk=vaca.id).exists())

    def test_numero_de_registro_e_unico(self):
        self.autenticar(self.admin)
        resposta = self.client.post(
            "/animals/",
            {"name": "Duplicada", "breed": self.raca.id, "register_number": 1},
            format="json",
        )
        self.assertEqual(resposta.status_code, 400)

    def test_criar_editar_e_excluir_touro(self):
        self.autenticar(self.admin)
        antes = self.client.get("/bulls/").data
        criado = self.client.post(
            "/bulls/",
            {"name": "Imperador", "breed": self.raca.id, "register_number": 200, "active": True},
            format="json",
        )
        self.assertEqual(criado.status_code, 201, criado.data)
        pk = criado.data["id"]

        depois = self.client.get("/bulls/").data
        self.assertEqual(len(depois), len(antes) + 1)
        self.assertIn(pk, [item["id"] for item in depois])

        editado = self.client.patch(f"/bulls/{pk}/", {"active": False}, format="json")
        self.assertEqual(editado.status_code, 200)
        self.assertFalse(Bull.objects.get(pk=pk).active)

        self.assertEqual(self.client.delete(f"/bulls/{pk}/").status_code, 204)
        self.assertFalse(Bull.objects.filter(pk=pk).exists())

    def test_atendimento_veterinario_retorna_veterinario_e_dados_do_animal(self):
        self.autenticar(self.operador)
        criado = self.client.post(
            "/animal_health/",
            {
                "animal": self.vaca1.id,
                "consultation_date": "2026-11-20",
                "consultation_reason": "Mastite",
                "consultation_solution": "Antibiótico intramamário por 3 dias",
                "veterinarian": "Dr. Carlos Silva",
            },
            format="json",
        )
        self.assertEqual(criado.status_code, 201, criado.data)
        self.assertEqual(criado.data["veterinarian"], "Dr. Carlos Silva")
        self.assertEqual(criado.data["consultation_solution"], "Antibiótico intramamário por 3 dias")
        self.assertEqual(criado.data["animal_name"], self.vaca1.name)
        self.assertEqual(criado.data["animal_register"], self.vaca1.register_number)
        self.assertEqual(AnimalHealth.objects.count(), 1)


class FiltroPorAnimalTests(BaseAPITestCase):
    """`?animal_id=` precisa filtrar (antes devolvia os registros de todos)."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        WeightHistory.objects.create(animal=cls.vaca1, weight=450, weighing_date=date(2026, 1, 10))
        WeightHistory.objects.create(animal=cls.vaca1, weight=460, weighing_date=date(2026, 2, 10))
        WeightHistory.objects.create(animal=cls.vaca2, weight=500, weighing_date=date(2026, 1, 10))

    def test_filtra_pelo_animal(self):
        self.autenticar(self.operador)
        resposta = self.client.get(f"/weight_history/?animal_id={self.vaca1.id}")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.data), 2)
        self.assertTrue(all(item["animal"] == self.vaca1.id for item in resposta.data))

    def test_sem_filtro_devolve_todos(self):
        self.autenticar(self.operador)
        self.assertEqual(len(self.client.get("/weight_history/").data), 3)

    def test_filtro_ignorado_em_modelo_sem_animal(self):
        self.autenticar(self.operador)
        resposta = self.client.get(f"/breeds/?animal_id={self.vaca1.id}")
        self.assertEqual(len(resposta.data), 1)


class VacinacaoTests(BaseAPITestCase):
    def test_filtro_upcoming(self):
        vacina = Vaccine.objects.create(name="Aftosa")
        hoje = date.today()
        Vaccination.objects.create(
            animal=self.vaca1, vaccine=vacina, dosage=5,
            vaccination_date=date(2025, 1, 1), next_vaccination_date=date(2025, 6, 1),
        )
        futura = Vaccination.objects.create(
            animal=self.vaca2, vaccine=vacina, dosage=5,
            vaccination_date=hoje, next_vaccination_date=date(hoje.year + 1, 1, 1),
        )
        self.autenticar(self.operador)
        resposta = self.client.get("/vaccinations/?upcoming=true")
        self.assertEqual([item["id"] for item in resposta.data], [futura.id])


class MigrationsDeDadosTests(TestCase):
    def test_grupos_de_papel_existem(self):
        self.assertTrue(Group.objects.filter(name=ADMINISTRADOR).exists())
        self.assertTrue(Group.objects.filter(name=OPERADOR).exists())

    def test_tipos_de_movimentacao_padrao(self):
        self.assertTrue(MovementType.objects.filter(name="Troca de pasto").exists())
