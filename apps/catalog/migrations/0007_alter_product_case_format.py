# Generated by Django 5.0.4 on 2024-05-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_product_case_format_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='case_format',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Европа'), (2, 'Азия'), (3, 'Америка'), (4, 'Грузовые')], null=True, verbose_name='Формат корпуса'),
        ),
    ]