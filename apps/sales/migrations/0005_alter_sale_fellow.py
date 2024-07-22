# Generated by Django 5.0.2 on 2024-02-24 22:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0001_initial'),
        ('sales', '0004_sale_scrap_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='fellow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='root.fellow', verbose_name='Сотрудник'),
        ),
    ]
