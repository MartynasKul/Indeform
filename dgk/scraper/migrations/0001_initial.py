# Generated by Django 5.1.5 on 2025-01-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skelbimas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(max_length=255)),
                ('vykdytojoPavadinimas', models.CharField(max_length=255)),
                ('nuoroda', models.URLField()),
                ('data', models.DateField()),
                ('terminas', models.DateField()),
                ('bvpzkodas', models.CharField(max_length=50)),
            ],
        ),
    ]
