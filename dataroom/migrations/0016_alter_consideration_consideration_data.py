from django.db import migrations, models

def fill_null_values(apps, schema_editor):
    Consideration = apps.get_model('dataroom', 'Consideration')
    for consideration in Consideration.objects.filter(consideration_data__isnull=True):
        consideration.consideration_data = b''  # ou qualquer valor padrão apropriado
        consideration.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dataroom', '0011_auto_20240703_2043'),  # substitua pelo nome da sua última migration
    ]

    operations = [
        migrations.RunPython(fill_null_values),
        migrations.AlterField(
            model_name='consideration',
            name='consideration_data',
            field=models.BinaryField(null=True, blank=True),
        ),
    ]
