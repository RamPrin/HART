# Generated by Django 5.0.3 on 2024-03-20 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('king', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='king',
            name='kingdom',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='king.kingdom'),
        ),
    ]
