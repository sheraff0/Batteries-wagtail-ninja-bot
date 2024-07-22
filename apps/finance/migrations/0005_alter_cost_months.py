# Generated by Django 5.0.4 on 2024-04-07 18:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_cost_months'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='months',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='На сколько месяцев?'),
        ),
    ]