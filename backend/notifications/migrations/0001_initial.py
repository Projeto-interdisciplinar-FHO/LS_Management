from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Mensagem da notificação para o administrador')),
                ('notification_type', models.CharField(choices=[('weight', 'Pesagem Registrada'), ('vaccination', 'Vacinação Aplicada'), ('feeding', 'Alimentação Registrada'), ('health', 'Problema de Saúde Identificado'), ('movement', 'Movimento de Animal'), ('milk', 'Ordenha Registrada'), ('batch_vaccination', 'Vacinação em Lote'), ('animal_created', 'Animal Cadastrado')], default='weight', help_text='Tipo de notificação', max_length=20)),
                ('read', models.BooleanField(default=False, help_text='Indica se a notificação foi lida')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Data e hora de criação')),
                ('animal', models.ForeignKey(blank=True, help_text='Animal relacionado à notificação', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications', to='animals.animal')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['-created_at'], name='notificatio_created_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['read', '-created_at'], name='notificatio_read_idx'),
        ),
    ]
