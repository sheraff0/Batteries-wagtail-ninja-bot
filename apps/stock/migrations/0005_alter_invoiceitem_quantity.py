# Generated by Django 5.0.4 on 2024-04-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_invoice_scrap_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='quantity',
            field=models.SmallIntegerField(default=1, verbose_name='Количество'),
        ),
    ]
