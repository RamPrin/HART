# Generated by Django 5.0.3 on 2024-03-20 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('king', '0002_alter_king_kingdom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servant',
            name='kingdom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='king.kingdom'),
        ),
    ]
