from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0006_remove_weight_and_legacy_tables'),
    ]

    operations = [
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS tasks_task',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]