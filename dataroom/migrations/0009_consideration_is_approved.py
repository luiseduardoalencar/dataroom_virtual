# Generated by Django 5.0.6 on 2024-07-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataroom", "0008_file_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="consideration",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]