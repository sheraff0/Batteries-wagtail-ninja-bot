# Generated by Django 5.0.2 on 2024-02-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_invoice_scrap_value_alter_invoice_scrap_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='scrap_quantity',
            field=models.SmallIntegerField(default=0, verbose_name='Лом, штуки'),
        ),
    ]
