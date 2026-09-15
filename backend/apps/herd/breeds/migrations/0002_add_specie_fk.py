from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('breeds', '0001_initial'),
        ('species', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breed',
            name='specie',
            field=models.ForeignKey(
                blank=True,
                help_text='Espécie à qual esta raça pertence',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='breeds',
                to='species.specie'
            ),
        ),
        migrations.AlterModelOptions(
            name='breed',
            options={'ordering': ['specie', 'name'], 'verbose_name_plural': 'Breeds'},
        ),
    ]
