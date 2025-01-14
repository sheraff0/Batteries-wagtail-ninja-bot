# Generated by Django 5.0.2 on 2024-02-22 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='scrap_value',
            field=models.IntegerField(default=0, verbose_name='Оценка лома'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='scrap_weight',
            field=models.SmallIntegerField(default=0, verbose_name='Прием лома, кг'),
        ),
    ]
