# Generated by Django 3.2.7 on 2021-11-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20211111_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drink',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
    ]
