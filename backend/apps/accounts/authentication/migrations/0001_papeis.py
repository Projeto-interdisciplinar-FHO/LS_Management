from django.db import migrations


ADMINISTRADOR = "Administrador"
OPERADOR = "Operador"


def criar(apps, schema_editor):
    group_model = apps.get_model("auth", "Group")
    for nome in (ADMINISTRADOR, OPERADOR):
        group_model.objects.get_or_create(name=nome)


def remover(apps, schema_editor):
    group_model = apps.get_model("auth", "Group")
    group_model.objects.filter(name__in=(ADMINISTRADOR, OPERADOR)).delete()


class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0001_initial")]
    operations = [migrations.RunPython(criar, remover)]
