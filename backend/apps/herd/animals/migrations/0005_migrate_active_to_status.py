from django.db import migrations


def migrate_active_to_status(apps, schema_editor):
    Animal = apps.get_model('animals', 'Animal')
    for animal in Animal.objects.all():
        if animal.active:
            animal.status = 'ativo'
        else:
            animal.status = 'inativo'
        animal.save(update_fields=['status'])


def reverse_migrate_status_to_active(apps, schema_editor):
    Animal = apps.get_model('animals', 'Animal')
    for animal in Animal.objects.all():
        animal.active = animal.status == 'ativo'
        animal.save(update_fields=['active'])


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0004_animal_status_alter_animal_active'),
    ]

    operations = [
        migrations.RunPython(migrate_active_to_status, reverse_migrate_status_to_active),
    ]
