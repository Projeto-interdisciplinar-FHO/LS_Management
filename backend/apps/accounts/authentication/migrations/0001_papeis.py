"""Cria os dois perfis do TAP como grupos, na migração.

Em migração e não em script à parte para que qualquer pessoa que rode
`manage.py migrate` — na máquina dela, no servidor, no CI — tenha os grupos
sem precisar saber que eles existem.
"""

from django.db import migrations

ADMINISTRADOR = "Administrador"
OPERADOR = "Operador"


def criar(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for nome in (ADMINISTRADOR, OPERADOR):
        Group.objects.get_or_create(name=nome)


def remover(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=(ADMINISTRADOR, OPERADOR)).delete()


class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0001_initial")]
    operations = [migrations.RunPython(criar, remover)]
