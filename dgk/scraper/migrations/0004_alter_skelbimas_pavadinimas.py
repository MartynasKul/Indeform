# Generated by Django 5.1.5 on 2025-01-16 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_rename_bvpzkodas_skelbimas_bvpzkodas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skelbimas',
            name='pavadinimas',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]