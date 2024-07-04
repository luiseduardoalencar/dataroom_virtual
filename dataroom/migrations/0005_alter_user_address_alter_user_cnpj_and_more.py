# Generated by Django 5.0.6 on 2024-07-02 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "dataroom",
            "0004_user_address_user_cnpj_user_company_name_user_phone_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.CharField(default="Default Address", max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="cnpj",
            field=models.CharField(default="00.000.000/0000-00", max_length=18),
        ),
        migrations.AlterField(
            model_name="user",
            name="company_name",
            field=models.CharField(default="Default Company", max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(default="(00) 0000-0000", max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="social_reason",
            field=models.CharField(default="Default Social Reason", max_length=255),
        ),
    ]