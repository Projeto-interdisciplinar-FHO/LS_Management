from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_health', '0002_remove_animalhealth_disease_prediction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalhealth',
            name='consultation_solution',
            field=models.TextField(blank=True, default=''),
        ),
    ]
