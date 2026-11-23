"""Preenche os tipos de movimentacao com os que existem numa fazenda leiteira.

A tabela estava vazia e nao ha tela para cadastra-la — mas `animal_movements`
exige `movement_type`, entao qualquer movimentacao falhava com 400. Um dado
obrigatorio que ninguem consegue criar trava a funcionalidade inteira.

Os nomes vem da rotina de gado de leite: o animal sai do lote de ordenha para
o de secagem antes do parto, vai para a enfermaria quando adoece, e assim por
diante. `get_or_create` para nao duplicar se alguem ja tiver cadastrado.
"""

from django.db import migrations

TIPOS = [
    "Troca de pasto",
    "Entrada na ordenha",
    "Saida da ordenha",
    "Secagem",
    "Enfermaria",
    "Quarentena",
    "Venda",
    "Nascimento",
    "Obito",
]


def criar(apps, schema_editor):
    MovementType = apps.get_model("movement_types", "MovementType")
    for nome in TIPOS:
        MovementType.objects.get_or_create(name=nome)


def remover(apps, schema_editor):
    MovementType = apps.get_model("movement_types", "MovementType")
    MovementType.objects.filter(name__in=TIPOS).delete()


class Migration(migrations.Migration):
    dependencies = [("movement_types", "0001_initial")]
    operations = [migrations.RunPython(criar, remover)]
