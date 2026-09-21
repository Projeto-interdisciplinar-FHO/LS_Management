from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0005_migrate_active_to_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='weight',
        ),
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS animal_biometrics_animalalert',
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS animal_biometrics_biometricreading',
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS notifications_notification',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]